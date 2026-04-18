# 方法一：递推
def ways_iterative(n):
	# 边界条件：没有台阶时记为 0 种
	if n <= 0:
		return 0
	if n == 1:
		return 1
	if n == 2:
		return 2
	if n == 3:
		return 4

	# 序列解包：a,b,c 分别表示 f(n-3), f(n-2), f(n-1)
	a, b, c = 1, 2, 4
	# 类似于滑动窗口，目标是c
	for _ in range(4, n + 1):
		a, b, c = b, c, a + b + c
	return c

# 方法二：递归
def ways_recursive(n, memo=None):
	# 使用字典做记忆化，避免重复递归
	if memo is None:
		memo = {1: 1, 2: 2, 3: 4}

	if n <= 0:
		return 0
	if n in memo:
		return memo[n]

	memo[n] = (
		ways_recursive(n - 1, memo)
		+ ways_recursive(n - 2, memo)
		+ ways_recursive(n - 3, memo)
	)
	return memo[n]


n = 15
ans_iter = ways_iterative(n)
ans_rec = ways_recursive(n)

print(ans_iter)
print(ans_rec)
