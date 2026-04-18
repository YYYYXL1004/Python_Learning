import random

def get_initial_count():
	while True:
		try:
			n = int(input("请输入初始物品数(>=2)："))
			if n >= 2:
				return n
			print("初始物品数必须 >= 2")
		except ValueError:
			print("请输入整数")


def get_user_take(n):
	max_take = n // 2
	while True:
		try:
			take = int(input(f"你的回合，当前剩余 {n}，可拿 1~{max_take}："))
			if 1 <= take <= max_take:
				break
			print("输入不合法，请按规则重新输入")
		except ValueError:
			print("请输入整数")
	return take


def smart_take(n):
	max_take = n // 2
	k = n.bit_length()

	# 优先把剩余数量变成 2^m-1（如 3,7,15,31...）
	while k >= 1:
		target = (1 << k) - 1
		take = n - target
		if 1 <= take <= max_take:
			break
		k -= 1
	else:
		# 如果做不到，就随机拿一个合法数量
		take = random.randint(1, max_take)

	return take


def play_nim():
	n = get_initial_count()
	turn = "user"  # 轮到谁操作：user/computer

	while n > 1:
		if turn == "user":
			take = get_user_take(n)
			n -= take
			print(f"你拿走 {take} 个，剩余 {n} 个")
			turn = "computer"
		else:
			take = smart_take(n)
			n -= take
			print(f"计算机拿走 {take} 个，剩余 {n} 个")
			turn = "user"
	else:
		# while 正常结束（没有 break）会执行这里
		loser = "玩家" if turn == "user" else "计算机"
		winner = "计算机" if turn == "user" else "玩家"
		print(f"剩余 1 个，{loser}必须拿最后一个，判负。")
		print(f"{winner}获胜！")


play_nim()
