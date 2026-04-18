def classify_mail(content, rate=0.08):
	# 参数合法性检查
	if not isinstance(content, str):
		raise TypeError("content 必须是字符串")
	if not isinstance(rate, (int, float)):
		raise TypeError("rate 必须是数字")
	if rate < 0 or rate > 1:
		raise ValueError("rate 必须在 [0, 1] 范围内")

	# 先做简单清洗：去首尾空白，并移除中间空格和制表符
	text = content.strip().replace(" ", "").replace("\t", "")
	if len(text) == 0:
		return "正常邮件", 0.0

	noise_chars = "【】*/-"
	# 使用 map + lambda 生成布尔序列，sum 统计干扰符号数量
	noise_count = sum(map(lambda ch: ch in noise_chars, text))
	noise_rate = noise_count / len(text)

	# rate 越小越严格，越容易判为垃圾邮件
	result = "垃圾邮件" if noise_rate >= rate else "正常邮件"
	return result, noise_rate


mail_content = input().rstrip("\n")

# 第二行可选输入 rate，不输入时使用默认值
try:
	rate_line = input().strip()
except EOFError:
	rate_line = ""

try:
	if rate_line:
		used_rate = float(rate_line)
	else:
		used_rate = classify_mail.__defaults__[0]

	result, detected_rate = classify_mail(mail_content, used_rate)
	print(f"检测值={detected_rate:.2f}, 阈值={used_rate:.2f}, {result}")
except (TypeError, ValueError):
	print("输入不合法")
