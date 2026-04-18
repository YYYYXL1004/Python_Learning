def typing_score(origin, user_input):
	# 在函数中检查参数合法性
	if not isinstance(origin, str) or not isinstance(user_input, str):
		raise TypeError("origin 和 user_input 必须是字符串")
	if len(origin) == 0:
		raise ValueError("origin 不能为空")
	if len(user_input) > len(origin):
		raise ValueError("user_input 长度不能大于 origin")

	# zip 对齐比较，生成器表达式逐位产生 True/False，sum 统计正确数量
	correct_count = sum(a == b for a, b in zip(origin, user_input))
	return round(correct_count / len(origin) * 100, 2) # 保留2位小数

origin = input().rstrip("\n")
user_input = input().rstrip("\n")

try:
	score = typing_score(origin, user_input)
	print(f"{score:.2f}%")
except (TypeError, ValueError):
	print("输入不合法")
