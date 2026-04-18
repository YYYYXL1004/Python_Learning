import string

text = input().rstrip("\n")
# 把密钥限制在 0~25，支持输入任意整数
key = int(input()) % 26

# 把整个字母表存到lower和upper中
lower = string.ascii_lowercase
upper = string.ascii_uppercase

# 用切片把字母表循环右移 key 位，构造加密后的字母表
lower_shift = lower[key:] + lower[:key]
upper_shift = upper[key:] + upper[:key]

# 生成大小写映射表；非字母字符会在 translate 中保持不变
# 用 maketrans 建好“原字母 -> 偏移后字母”的对应关系。
# 用 translate 一次性把整句明文替换成密文。
trans_table = str.maketrans(lower + upper, lower_shift + upper_shift)
print(text.translate(trans_table))
