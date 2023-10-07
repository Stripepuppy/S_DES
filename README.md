# 程序测试结果

## 第1关：基本测试

根据S-DES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是8bit的数据和10bit的密钥，输出是8bit的密文。

二进制交互界面
![273377380-67233e87-850e-4482-9994-5fcca8626355](https://github.com/Stripepuppy/S_DES/assets/133982775/a34bc31e-77a6-4bb4-a5ea-fe4c9a6cecea)

明文、密文输入格式错误提示。
![273376676-339c4f18-13c4-4d76-a336-c8b949fdd2ee](https://github.com/Stripepuppy/S_DES/assets/133982775/1ca76ba5-a573-4d00-a0a7-9271bd1638a5)

密钥输入格式错误提示。
![273376564-db1cfe8c-146f-4a8f-b546-934d6510d3e8](https://github.com/Stripepuppy/S_DES/assets/133982775/646bbccd-122e-4924-a128-b4543cbb3848)

## 第2关：交叉测试

本组二进制明文加密结果。
![273377769-3d5b6afa-16f1-4d43-aea6-2ba31aa67e4a](https://github.com/Stripepuppy/S_DES/assets/133982775/a429b80f-c6a2-49dd-84ce-756995599a9c)

交叉测试组二进制明文加密结果。
<img width="300" alt="273377241-ae60deaf-a928-4567-825b-c255248d8db5" src="https://github.com/Stripepuppy/S_DES/assets/133982775/f02674a6-1596-4298-b89d-05a36033dd3b">

本组字符串明文加密结果。
![273377863-1dcaf6fa-16a2-43d5-9ba0-8486972561df](https://github.com/Stripepuppy/S_DES/assets/133982775/fde6d666-651c-4d79-a0f7-63b0121753f4)

交叉验证组字符串加密结果。
<img width="297" alt="273377286-f142a77a-6c5e-4655-9c82-0e0222d9ba96" src="https://github.com/Stripepuppy/S_DES/assets/133982775/17b44724-5250-4dc9-9500-f638dbedbf65">

## 第3关：扩展功能

考虑到向实用性扩展，加密算法的数据输入可以是ASCII编码字符串(分组为1 Byte)，对应地输出也可以是ASCII字符串(很可能是乱码)。

字符串交互界面
![273376628-388fa005-e30d-4bde-8246-ce2f7f755f43](https://github.com/Stripepuppy/S_DES/assets/133982775/b4acdc52-20d3-43bd-b58c-28d04f226f10)

## 第4关：暴力破解

使用相同密钥的明、密文对(一个或多个)，可使用暴力破解的方法找到正确的密钥Key。

一对密文和密钥。
![273378083-31c4812e-d9f0-4373-a163-59e8afb9b676](https://github.com/Stripepuppy/S_DES/assets/133982775/46a9a935-b947-472b-8a62-a6aa5384f975)

多对密文和密钥。（在后台进行测试）
明文：[00001111, 00010000, 00010001] 密文：[10101101, 00100001, 10011001] 密钥：0001000111
<img width="512" alt="image" src="https://github.com/Stripepuppy/S_DES/assets/133982775/0239bc69-4ef8-4882-92d5-df57abba9a38">

## 第5关：封闭测试

根据第4关的结果，进一步分析，随机选择的一个明密文对，有不止一个密钥Key
![273378358-a7fe0004-5986-41c6-be9b-fcbe478705f9](https://github.com/Stripepuppy/S_DES/assets/133982775/f49423b3-fb01-4d30-b972-b64f6b3ff557)

在进一步的分析中，我们发现：对于不同的10位密钥，只要生成的两个子密钥Km和Kn是相同的，那么使用这两个密钥加密相同的明文将产生相同的密文。

具体来说，我们比较了以下五对密钥生成的子密钥：

1. 1000101010 和 1100101010
2. 1111110011 和 1011110011
3. 1000000010 和 1100000010
4. 0011100000 和 0111100000
5. 0010101101 和 0110101101

总结：当两个10位密钥只有在第2位上存在差异，而其他位都相同时，它们会生成相同的子密钥。这个现象引发了我们对S-DES算法的进一步思考，尤其是子密钥生成的过程。这种情况可能会导致一些安全性问题，因此在使用S-DES时需要格外小心，并确保密钥的随机性和安全性以避免潜在的风险。


# S-DES加解密工具开发手册

本开发手册旨在帮助您了解和使用S-DES（Simplified Data Encryption Standard）加解密算法的Flask应用程序，以及使用暴力破解方式找到可能的密钥。下面是关于如何使用这个应用程序的详细说明。

## 目录

1. 概述
2. 安装依赖
3. 启动应用程序
4. 前端页面设计
   - 4.1 字符串输入页面 (string.html)
   - 4.2 二进制输入页面 (binary.html)
5. 加解密算法
   - 5.1 算法简介
   - 5.2 参数设置
   - 5.3 轮函数 F
   - 5.4 密钥生成
   - 5.5 S-DES加密算法
   - 5.6 S-DES解密算法
6. 暴力破解
   - 6.1 暴力破解概述
   - 6.2 使用暴力破解功能
     - 6.2.1 暴力破解字符串密钥
     - 6.2.2 暴力破解二进制密钥
   - 6.3 安全注意事项
7. 用户指南
   - 7.1 字符串输入模式
   - 7.2 二进制输入模式
8. 注意事项
9. 安全性注意事项
10. 结束应用程序
11. 总结

## 1. 概述

S-DES是一个轻量级的对称密钥加密算法，用于加密和解密文本数据。这个应用程序实现了S-DES的加解密功能，并提供了两种不同的输入模式：字符串输入和二进制输入。此外，您还可以使用暴力破解方式来尝试找到可能的密钥。

## 2. 安装依赖

在开始使用该应用程序之前，您需要安装以下依赖项：

- Python 3.x
- Flask

您可以使用以下命令来安装Flask：

```bash
pip install Flask
```

## 3. 启动应用程序

要运行该应用程序，使用以下命令在终端中进入应用程序所在的目录，并执行以下命令：

```bash
python app.py
```

应用程序将在本地启动一个Flask服务器，并在默认端口（通常为5000）上运行。您可以通过访问 `http://localhost:5000/` 在浏览器中打开应用程序的主页。

## 4. 前端页面设计

### 4.1. 字符串输入页面 (string.html)

这个页面允许用户输入字符串明文和10位二进制密钥，然后执行S-DES加密和解密操作。以下是页面中的一些关键元素和功能的原始代码：

#### 4.1.1. 表单提交加密请求

```html
<form id="encrypt-form" action="/encrypt_string" method="POST">
    <!-- 输入字段 -->
    <input type="text" class="form-control" id="plaintext-encrypt" name="plaintext">
    <input type="text" class="form-control" id="key-encrypt" name="key" maxlength="10">
    <!-- 加密按钮 -->
    <button type="submit" class="btn btn-block btn-lg bg-primary mt-4 text-white">Encrypt</button>
</form>
```

#### 4.1.2. 表单提交解密请求（使用jQuery）

```html
<form id="decrypt-form">
    <!-- 输入字段 -->
    <input type="text" class="form-control" id="ciphertext-decrypt" name="ciphertext">
    <input type="text" class="form-control" id="key-decrypt" name="key" maxlength="10">
    <!-- 解密按钮 -->
    <button type="submit" class="btn btn-block btn-lg bg-primary mt-4 text-white">Decrypt</button>
</form>
```

#### 4.1.3. 表单提交暴力破解请求（使用jQuery）

```html
<form id="brute-force-form">
    <!-- 输入字段 -->
    <input type="text" class="form-control" id="brute-force-plaintext" name="plaintext">
    <input type="text" class="form-control" id="brute-force-ciphertext" name="ciphertext">
    <!-- 暴力破解按钮 -->
    <button type="submit" class="btn btn-block btn-lg bg-primary mt-4 text-white">Find Possible Keys</button>
</form>
```

### 4.2. 二进制输入页面 (binary.html)

这个页面允许用户输入二进制明文和密钥，然后执行S-DES加密和解密操作。以下是页面中的一些关键元素和功能的原始代码：

#### 4.2.1. 表单提交加密请求

```html
<form id="encrypt-binary-form">
    <!-- 输入字段 -->
    <input type="text" class="form-control" id="plaintext-bin-encrypt" name="plaintext_bin">
    <input type="text" class="form-control" id="key-encrypt-binary" name="key" maxlength="10">
    <!-- 加密按钮 -->
    <button type="submit" class="btn btn-block btn-lg bg-primary mt-4 text-white">Encrypt</button>
</form>
```

#### 4.2.2. 表单提交解密请求（使用jQuery）

```html
<form id="decrypt-binary-form">
    <!-- 输入字段 -->
    <input type="text" class="form-control" id="ciphertext-bin-decrypt" name="ciphertext_bin">
    <input type="text" class="form-control" id="key-decrypt-binary" name="key" maxlength="10">
    <!-- 解密按钮 -->
    <button type="submit" class="btn btn-block btn-lg bg-primary mt-4 text-white">Decrypt</button>
</form>
```

#### 4.2.3. 表单提交暴力破解请求（使用jQuery）

```html
<form id="brute-force-binary-form">
    <!-- 输入字段 -->
    <input type="text" class="form-control" id="brute-force-plaintext-bin" name="plaintext_bin">
    <input type="text" class="form-control" id="brute-force-ciphertext-bin" name="ciphertext_bin">
    <!-- 暴力破解按钮 -->
    <button type="submit" class="btn btn-block btn-lg bg-primary mt-4 text-white">Find Possible Keys</button>
</form>
```

## 5. 加解密算法

### 5.1. 算法简介

S-DES（Simplified Data Encryption Standard）是一种简化的数据加密标准，用于对小块数据进行加密和解密。它采用10位密钥，使用多轮置换和S盒代替等操作来实现加密和解密过程。

### 5.2. 参数设置

```python
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
        [2, 3, 1, 0],
        [3, 0, 1, 2],
        [2, 1, 0, 3]
    ]
    self.P4 = [1, 3, 2, 0]
```

### 5.3. 轮函数 F

```python
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
```

轮函数F（Feistel Function）是S-DES算法中的关键组成部分，用于混淆和置换数据。它在加密和解密过程中都起着重要的作用。轮函数F的主要任务是将数据与子密钥进行混合，并应用S-盒替代操作。

### 5.4. 密钥生成

```python
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
```

密钥生成函数接受一个10位的密钥作为输入，首先进行初始的置换（P10），然后将密钥分成两部分，并对每部分进行循环左移一位，接着再次进行置换（P8），生成两个子密钥 k1 和 k2。

### 5.5. S-DES加密算法

```python
def encrypt(self, plaintext_bin, key):
    k1, k2 = self.key_generation(key)
    data = self.permute(plaintext_bin, self.IP)
    temp = self.fk(data, k1)
    temp = temp[4:] + temp[:4]
    data = self.fk(temp, k2)
    return self.permute(data, self.IPinverse)

def encrypt_ascii(self, plaintext, key):
    # 转换明文为二进制字符串
    plaintext_bin = self.char_to_bin(plaintext)
    # 加密并返回ASCII字符
    ciphertext_bin = self.encrypt(plaintext_bin, key)
    return self.bin_to_char("".join(ciphertext_bin))

def encrypt_string(self, plaintext, key):
    """加密整个字符串"""
    self.validate_input(key, 10)
    return ''.join([self.encrypt_ascii(char, key) for char in plaintext])
```

加密函数接受明文和密钥作为输入，首先对明文进行初始置换（IP），然后进入Fk函数，该函数使用子密钥 k1 和 k2 来执行一轮的加密操作。最后，再次进行逆初始置换（IPinverse），得到加密后的密文。

### 5.6. S-DES解密算法

```python
def decrypt(self, ciphertext_bin, key):
    k1, k2 = self.key_generation(key)
    data = self.permute(ciphertext_bin, self.IP)
    temp = self.fk(data, k2)
    temp = temp[4:] + temp[:4]
    data = self.fk(temp, k1)
    return self.permute(data, self.IPinverse)

def decrypt_ascii(self, ciphertext, key):
    # 转换密文为二进制字符串
    ciphertext_bin = self.char_to_bin(ciphertext)
    # 解密并返回ASCII字符
    decryptedtext_bin = self.decrypt(ciphertext_bin, key)
    return self.bin_to_char("".join(decryptedtext_bin))

def decrypt_string(self, ciphertext, key):
    """解密整个字符串"""
    self.validate_input(key, 10)
    return ''.join([self.decrypt_ascii(char, key) for char in ciphertext])
```

解密函数与加密函数非常相似，唯一的区别是在解密中使用的是相反顺序的子密钥 k2 和 k1，以及解密后需要执行逆初始置换（IPinverse）来还原明文。

## 6. 暴力破解

### 6.1. 暴力破解概述

S-DES暴力破解是一种尝试所有可能的密钥来解密已知明文和密文对的过程。在S-DES中，密钥长度为10位，因此总共有1024种可能的密钥。通过尝试这些密钥，我们可以找到正确的密钥来解密给定的密文。

### 6.2. 使用暴力破解功能

#### 6.2.1. 暴力破解字符串密钥

您可以使用以下代码示例来执行暴力破解ASCII字符串密钥的操作：

```python
pythonCopy codefrom flask import Flask, render_template, request, jsonify
import concurrent.futures

# ...

@app.route('/brute_force_string', methods=['POST'])
def brute_force_string():
    plaintext = request.form.get('plaintext')
    ciphertext = request.form.get('ciphertext')
    known_pairs = [(plaintext, ciphertext)]
    keys = brute_force_decrypt(known_pairs, sdes)
    return jsonify(keys=keys)

# ...
```

在上述代码中，`plaintext` 是已知的明文，`ciphertext` 是相应的密文。`brute_force_decrypt` 函数将尝试所有可能的密钥，找到匹配的密钥，并将其返回。

#### 6.2.2. 暴力破解二进制密钥

如果您希望使用二进制输入进行暴力破解，您可以使用以下代码示例：

```python
pythonCopy codefrom flask import Flask, render_template, request, jsonify

# ...

@app.route('/brute_force_binary', methods=['POST'])
def brute_force_binary():
    plaintext_bin = request.form.get('plaintext_bin')
    ciphertext_bin = request.form.get('ciphertext_bin')
    keys = brute_force_decrypt_binary(plaintext_bin, ciphertext_bin, sdes)
    return jsonify(keys=keys)

# ...
```

在上述代码中，`plaintext_bin` 和 `ciphertext_bin` 分别是已知的二进制明文和密文。`brute_force_decrypt_binary` 函数将尝试所有可能的二进制密钥，找到匹配的密钥，并将其返回。

### 6.3. 安全注意事项

请注意，暴力破解是一种计算密集型操作，特别是对于10位密钥。因此，可能需要相当长的时间来完成暴力破解。此外，使用暴力破解时，需要确保已知的明文和密文对是准确的，否则可能无法找到正确的密钥。

## 7. 用户指南

### 7.1 字符串输入模式

在主页上选择 "String Input" 选项卡，然后您可以执行以下操作：

- **加密字符串**：输入明文文本和10位二进制密钥，然后单击 "Encrypt" 按钮来加密文本。

- **解密字符串**：输入密文文本和10位二进制密钥，然后单击 "Decrypt" 按钮来解密文本。

- **暴力破解字符串**：输入已知的明文和对应的密文，然后单击 "Brute Force Decrypt" 按钮来尝试找到可能的密钥。

### 7.2 二进制输入模式

在主页上选择 "Binary Input" 选项卡，然后您可以执行以下操作：

- **加密二进制数据**：输入明文的二进制表示和10位二进制密钥，然后单击 "Encrypt" 按钮来加密数据。

- **解密二进制数据**：输入密文的二进制表示和10位二进制密钥，然后单击 "Decrypt" 按钮来解密数据。

- **暴力破解二进制数据**：输入已知的明文的二进制表示和对应的密文的二进制表示，然后单击 "Brute Force Decrypt" 按钮来尝试找到可能的密钥。

## 8. 注意事项

- 密钥长度为10位，只能包含0和1。
- 当使用暴力破解功能时，应考虑到需要尝试所有可能的密钥，因此速度可能较慢。

## 9. 安全性注意事项

请注意，S-DES是一种较旧的加密算法，不适用于安全性要求高的应用程序。在实际应用中，建议使用更强大的加密算法，如AES（高级加密标准）。

## 10. 结束应用程序

要停止应用程序，在终端中按下 `Ctrl+C`。

## 11. 总结

这个应用程序提供了一个用于学习和演示S-DES加解密算法的平台，以及一种尝试暴力破解可能的密钥的方法。请注意，这只是一个教育和演示用途的应用程序，不适用于实际安全需求。

希望这份开发手册能够帮助您使用S-DES加解密应用程序。如果您有任何疑问或需要进一步的帮助，请随时提问。

编写一份开发手册是一项详尽的任务，以下是一个基本的结构，其中包含了前端页面设计、加解密算法、暴力破解以及用户指南。每个部分都会包括相应功能的原始代码示例。
