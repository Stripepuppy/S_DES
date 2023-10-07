import concurrent.futures
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


class SDES:
    def __init__(self):
        # 定义各种置换表和S盒
        self.P10 = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
        self.P8 = [5, 2, 6, 3, 7, 4, 9, 8]
        self.IP = [1, 5, 2, 0, 3, 7, 4, 6]
        self.IPinverse = [3, 0, 2, 4, 6, 1, 7, 5]
        self.EP = [3, 0, 1, 2, 1, 2, 3, 0]
        self.S0 = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 0, 2]
        ]
        self.S1 = [
            [0, 1, 2, 3],
            [2, 0, 1, 3],
            [3, 0, 1, 2],
            [2, 1, 0, 3]
        ]
        self.P4 = [1, 3, 2, 0]

    def validate_input(self, data, length):
        """验证输入是否为指定长度的二进制字符串"""
        if not all([bit in ['0', '1'] for bit in data]):
            raise ValueError("输入只能包含0和1")
        if len(data) != length:
            raise ValueError(f"输入应为{length}位")

    def char_to_bin(self, char):
        """将ASCII字符转换为8位二进制字符串"""
        return format(ord(char), '08b')

    def bin_to_char(self, bin_str):
        """将8位二进制字符串转换为ASCII字符"""
        return chr(int(bin_str, 2))

    def permute(self, data, table):
        return [data[x] for x in table]

    def left_shift(self, data, n):
        return data[n:] + data[:n]

    def key_generation(self, key):
        key = self.permute(key, self.P10)
        left = key[:5]
        right = key[5:]
        left = self.left_shift(left, 1)
        right = self.left_shift(right, 1)
        k1 = self.permute(left + right, self.P8)
        left = self.left_shift(left, 1)
        right = self.left_shift(right, 1)
        k2 = self.permute(left + right, self.P8)
        return k1, k2

    def sbox_output(self, sbox, data):
        row = int(data[0] + data[3], 2)
        col = int(data[1] + data[2], 2)
        return format(sbox[row][col], '02b')

    def fk(self, data, key):
        left = data[:4]
        right = data[4:]
        right_expanded = self.permute(right, self.EP)
        result = [str(int(right_expanded[i]) ^ int(key[i])) for i in range(8)]
        left_result = self.sbox_output(self.S0, result[:4])
        right_result = self.sbox_output(self.S1, result[4:])
        result = self.permute(left_result + right_result, self.P4)
        final_result = [str(int(left[i]) ^ int(result[i])) for i in range(4)]
        return final_result + right

    def encrypt(self, plaintext_bin, key):
        k1, k2 = self.key_generation(key)
        data = self.permute(plaintext_bin, self.IP)
        temp = self.fk(data, k1)
        temp = temp[4:] + temp[:4]
        data = self.fk(temp, k2)
        return self.permute(data, self.IPinverse)

    def decrypt(self, ciphertext_bin, key):
        k1, k2 = self.key_generation(key)
        data = self.permute(ciphertext_bin, self.IP)
        temp = self.fk(data, k2)
        temp = temp[4:] + temp[:4]
        data = self.fk(temp, k1)
        return self.permute(data, self.IPinverse)

    def encrypt_ascii(self, plaintext, key):
        # 转换明文为二进制字符串
        plaintext_bin = self.char_to_bin(plaintext)
        # 加密并返回ASCII字符
        ciphertext_bin = self.encrypt(plaintext_bin, key)
        return self.bin_to_char("".join(ciphertext_bin))

    def decrypt_ascii(self, ciphertext, key):
        # 转换密文为二进制字符串
        ciphertext_bin = self.char_to_bin(ciphertext)
        # 解密并返回ASCII字符
        decryptedtext_bin = self.decrypt(ciphertext_bin, key)
        return self.bin_to_char("".join(decryptedtext_bin))

    def encrypt_string(self, plaintext, key):
        """加密整个字符串"""
        self.validate_input(key, 10)
        return ''.join([self.encrypt_ascii(char, key) for char in plaintext])

    def decrypt_string(self, ciphertext, key):
        """解密整个字符串"""
        self.validate_input(key, 10)
        return ''.join([self.decrypt_ascii(char, key) for char in ciphertext])


def brute_force_decrypt(known_pairs, sdes):
    """
    使用暴力破解找到所有可能的正确密钥。
    known_pairs 是一个列表，其中每个元素是一个 (plaintext, ciphertext) 对。
    """
    total_keys = 2 ** 10  # 10位密钥，总共有1024种可能
    valid_keys = []

    def check_key(key_bin):
        key_str = format(key_bin, '010b')
        for plaintext, ciphertext in known_pairs:
            if sdes.decrypt_string(ciphertext, key_str) != plaintext:
                return None
        return key_str

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for key in executor.map(check_key, range(total_keys)):
            if key:
                valid_keys.append(key)
    return valid_keys


@app.route('/')
def index():
    return render_template('string.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    plaintext = request.form.get('plaintext')
    key = request.form.get('key')
    sdes.validate_input(key, 10)
    ciphertext = sdes.encrypt_string(plaintext, key)
    return jsonify({'ciphertext': ciphertext})


@app.route('/decrypt', methods=['POST'])
def decrypt():
    plaintext = request.form.get('plaintext')
    ciphertext = request.form.get('ciphertext')
    known_pairs = [(plaintext, ciphertext)]
    keys = brute_force_decrypt(known_pairs, sdes)
    return jsonify({'keys': keys})


if __name__ == '__main__':
    sdes = SDES()
    app.run(debug=True)

# 交互部分
# sdes = SDES()

# try:
#     plaintext = input("请输入一个ASCII字符: ")
#     if len(plaintext) != 1:
#         raise ValueError("请输入单个字符")
#     key = input("请输入10位的密钥（二进制）: ")
#     sdes.validate_input(key, 10)
#     ciphertext = sdes.encrypt_ascii(plaintext, key)
#     decryptedtext = sdes.decrypt_ascii(ciphertext, key)
#     print("明文:", plaintext)
#     print("密文:", ciphertext)
#     print("解密后的文本:", decryptedtext)
# except ValueError as e:
#     print(f"输入错误: {e}")


# try:
#     plaintext = input("请输入一个字符串: ")
#     key = input("请输入10位的密钥（二进制）: ")
#     ciphertext = sdes.encrypt_string(plaintext, key)
#     decryptedtext = sdes.decrypt_string(ciphertext, key)
#     print("明文:", plaintext)
#     print("密文:", ciphertext)
#     print("解密后的文本:", decryptedtext)
# except ValueError as e:
#     print(f"输入错误: {e}")
#
#
# known_pairs = [(plaintext, ciphertext)]
# keys = brute_force_decrypt(known_pairs, sdes)
# print("Found key:", keys)
