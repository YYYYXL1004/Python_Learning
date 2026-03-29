import random

def input_int(msg):
	# 用异常处理约束输入必须为整数
	while True:
		try:
			n = int(input(msg))
		except ValueError:
			print("输入无效，请输入整数：")
		else:
			return n

def input_range():
	while True:
		left = input_int("请输入最小值：")
		right = input_int("请输入最大值：")
		if left < right:
			return left, right
		print("范围无效，要求最小值 < 最大值，请重新输入。")

def input_times():
	while True:
		times = input_int("请输入可猜次数(>0)：")
		if times > 0:
			return times
		print("次数必须大于0，请重新输入。")

def main():
	left, right = input_range()
	times = input_times()
	ans = random.randint(left, right)

	print(f"\n游戏开始！请在[{left}, {right}]内猜数字。")

	for i in range(1, times + 1):
		guess = input_int(f"第{i}次猜测：")
		if guess == ans:
			print("猜对了，游戏结束！")
			break
		# 条件表达式：根据大小关系给出提示
		print("太大了" if guess > ans else "太小了")
	else:
		# for 循环没有被 break 才会执行这里
		print(f"次数用完，游戏结束。正确答案是：{ans}")

if __name__ == "__main__":
	main()
