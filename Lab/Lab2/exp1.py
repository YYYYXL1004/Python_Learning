import random

def main():
	n = int(input("请输入掷飞镖次数："))

	hit_count = 0
	for _ in range(n):
		x = random.uniform(-1, 1)
		y = random.uniform(-1, 1)
		if x * x + y * y <= 1:
			hit_count += 1

	pi_estimate = 4 * hit_count / n
	print(f"模拟次数：{n}")
	print(f"圆周率近似值：{pi_estimate}")

if __name__ == "__main__":
	main()
