import random

def setup_doors():
    """初始化3扇门，随机放入1辆汽车和2只山羊"""
    car_door = random.randint(1, 3)
    doors = {1: '山羊', 2: '山羊', 3: '山羊'}
    doors[car_door] = '汽车'
    return doors, car_door

def play_monty_hall():
    """蒙蒂霍尔游戏主逻辑"""
    stats = {'换门并赢了': 0, '不换并赢了': 0}
    
    while True:
        try:
            print("\n--- 欢迎来到蒙蒂霍尔游戏！(输入 q 退出) ---")
            doors_dict, car_door = setup_doors()
            
            user_input = input("前面有1, 2, 3号门，请选择一扇：")
            if user_input.lower() == 'q':
                break
                
            choice = int(user_input)
            assert choice in [1, 2, 3], "只能选择 1, 2, 或 3 号门"
            
            all_doors = {1, 2, 3}
            host_options = all_doors - {choice} - {car_door}
            host_opens = random.choice(list(host_options))
            
            print(f"主持人打开了 {host_opens} 号门，后面是一只山羊！")
            
            switch_door = (all_doors - {choice} - {host_opens}).pop()
            switch_input = input(f"你想改选 {switch_door} 号门吗？(y/n): ")
            assert switch_input.lower() in ['y', 'n'], "只能输入 y 或 n"
            
            final_choice = switch_door if switch_input.lower() == 'y' else choice
            prize = doors_dict.get(final_choice)
            
            print(f"==> 你最终打开了 {final_choice} 号门，获得了：{prize}！\n")
            
            if prize == '汽车':
                if switch_input.lower() == 'y':
                    stats['换门并赢了'] += 1
                else:
                    stats['不换并赢了'] += 1

        except ValueError:
            print("输入非法：请输入有效的数字！")
        except AssertionError as e:
            print(f"输入非法：{e}")

    print("\n=== 游戏结束，你的战绩统计 ===")
    for key, value in stats.items():
        print(f"{key}: {value} 次")

if __name__ == "__main__":
    play_monty_hall()