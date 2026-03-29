import string

def get_level(pwd):
	# 用字典记录四类字符是否出现
	kinds = {
		"digit": False,
		"lower": False,
		"upper": False,
		"punc": False
	}
	# 遍历密码中的每个字符，用in判断类别
	for ch in pwd:
		if ch in string.digits:
			kinds["digit"] = True
		elif ch in string.ascii_lowercase:
			kinds["lower"] = True
		elif ch in string.ascii_uppercase:
			kinds["upper"] = True
		elif ch in string.punctuation:
			kinds["punc"] = True

	# and 的惰性求值：只要前面有 False，后面的判断就不再继续计算
	if kinds["digit"] and kinds["lower"] and kinds["upper"] and kinds["punc"]:
		kinds_count = 4
	else:
		kinds_count = sum(kinds.value())
	
	level_map = {
		4: "强密码",
		3: "中高",
		2: "中低",
		1: "弱密码",
		0: "弱密码",
	}
	return level_map[kinds_count], kinds_count

def main():
	pwd = input("请输入密码字符串：")
	level, kinds_count = get_level(pwd)

	print(f"字符种类数：{kinds_count}")
	print(f"安全强度：{level}")

if __name__ == "__main__":
	main()
