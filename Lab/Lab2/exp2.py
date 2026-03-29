from itertools import combinations, permutations

def step(num):
	# 先补充成4位，计算最大值减最小值
	s = str(num).zfill(4)
	small = int("".join(sorted(s)))
	large = int("".join(sorted(s, reverse=True)))
	return large - small

def build_numbers():
	# 不使用combinations的版本
	# numbers = []
	# for num in range(1000, 10000):
	# 	s = str(num)
	# 	if len(set(s)) == 4:
	# 		numbers.append(num)
	# return numbers

	# 先用 combinations 选4个互不相同的数字，再全排列成4位数
	numbers = set()
	# combinations(range(4), 3) --> (0,1,2), (0,1,3), (0,2,3), (1,2,3)
	for comb in combinations("0123456789", 4):
		# permutations(range(3), 2) --> (0,1), (0,2), (1,0), (1,2), (2,0), (2,1)
		for perm in permutations(comb, 4):
			if perm[0] == "0":
				continue
			numbers.add(int("".join(perm)))
	# 先用 set 去重，再用 sorted 排序。
	return sorted(numbers)

def verify_6174(numbers, limit=7):
	fail_cases = []
	for start in numbers:
		current = start
		reached = False
		# 限制做7次操作
		for _ in range(limit):
			current = step(current)
			if current == 6174:
				reached = True
				break
		if not reached:
			fail_cases.append(start)
	return fail_cases

def main():
	numbers = build_numbers()
	fail_cases = verify_6174(numbers)
	total = len(numbers)

	print(f"枚举的4位数个数：{total}")
	if not fail_cases:
		print("6174猜想正确")
	else:
		print("6174猜想不成立，以下数字未在7步之内到达6174：")
		print(fail_cases)

if __name__ == "__main__":
	main()

