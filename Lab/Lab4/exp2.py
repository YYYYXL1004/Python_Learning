import random

def simulate_wheel(trials=10000):
    """模拟转盘抽奖"""
    results = {}
    
    for _ in range(trials):
        # 生成 0 到 360 之间的随机浮点数表示指针位置
        angle = random.uniform(0, 360) 
        
        if 0 <= angle < 30:
            prize = '一等奖'
        elif 30 <= angle < 108:
            prize = '二等奖'
        else:
            prize = '三等奖'
            
        # 使用字典的 get() 方法累加中奖次数
        results[prize] = results.get(prize, 0) + 1
        
    return results

if __name__ == "__main__":
    trials = 10000
    final_results = simulate_wheel(trials)
    
    print(f"模拟转盘抽奖 {trials} 次的结果：")
    # 按照奖项顺序打印结果
    for prize in ['一等奖', '二等奖', '三等奖']:
        count = final_results.get(prize, 0)
        print(f"{prize}: {count} 次")