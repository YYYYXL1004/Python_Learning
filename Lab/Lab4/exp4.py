import random

def catch_fox(max_days):
    """模拟抓狐狸小游戏"""
    holes = [1, 2, 3, 4, 5]
    fox_pos = random.choice(holes)
    
    for day in range(1, max_days + 1):
        while True:
            try:
                choice = int(input(f"第 {day} 天，请选择要打开的洞口(1-5): "))
                if choice not in holes:
                    print("输入错误：只能选择 1 到 5 号洞口。")
                else:
                    break
            except ValueError:
                print("输入错误：请输入有效的数字。")
                
        if choice == fox_pos:
            print(f"恭喜！你在第 {day} 天抓到了狐狸！")
            break
        else:
            print("很遗憾，没有抓到。狐狸晚上逃到了隔壁洞口。")
            # 狐狸跳到隔壁洞口的逻辑
            if fox_pos == 1:
                fox_pos = 2
            elif fox_pos == 5:
                fox_pos = 4
            else:
                fox_pos += random.choice([-1, 1])
    else:
        # 带 else 子句的循环结构，循环正常结束（未触发 break）时执行
        print(f"游戏结束！规定的 {max_days} 次机会已用完，挑战失败。")

if __name__ == "__main__":
    try:
        max_days = int(input("请输入允许抓捕的最大天数: "))
        
        if max_days <= 0:
            print("输入错误：天数必须是正整数。")
        else:
            catch_fox(max_days)
            
    except ValueError:
        print("输入错误：请输入有效的数字。")