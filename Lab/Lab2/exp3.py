def input_count():
	# 人数必须是大于2的整数
	while True:
		try:
			n = int(input("请输入评委人数(>2)："))
			if n > 2:
				return n
			print("评委人数必须大于2，请重新输入。")
		except ValueError:
			print("输入无效，请输入整数。")

def input_scores(n):
	scores = []
	for i in range(n):
		while True:
			try:
				s = float(input(f"请输入第{i + 1}位评委的打分(0-100)："))
				if 0 <= s <= 100:
					scores.append(s)
					break
				print("分数必须在0到100之间，请重新输入。")
			except ValueError:
				print("输入无效，请输入数字。")
	return scores

def calc_score(scores):
	# 去掉一个最高分和一个最低分，再求平均
	left = scores.copy()
	left.remove(max(left))
	left.remove(min(left))
	return sum(left) / len(left)

def main():
	n = input_count()
	scores = input_scores(n)
	final_score = calc_score(scores)

	print("\n原始打分：", scores)
	print(f"最终得分：{final_score:.2f}")

if __name__ == "__main__":
	main()
