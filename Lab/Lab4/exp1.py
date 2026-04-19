import itertools

def josephus_slice(n, k):
    """方法一：使用列表切片模拟"""
    people = list(range(1, n + 1))
    
    while len(people) > 1:
        idx = (k - 1) % len(people)
        # 切片重组列表，被淘汰者后面的人排到前面
        people = people[idx + 1:] + people[:idx]
        
    return people[0]

def josephus_itertools(n, k):
    """方法二：使用 itertools.cycle 模拟"""
    people = list(range(1, n + 1))
    circle = itertools.cycle(range(n))
    left, cnt = n, 0
    
    while left > 1:
        idx = next(circle) # 使用内置函数 next() 推进迭代
        if people[idx] != 0:
            cnt += 1
            if cnt == k:
                people[idx] = 0 # 标记为淘汰
                cnt = 0
                left -= 1
                
    # 取出最后非 0 的幸存者
    return next(p for p in people if p != 0)

if __name__ == "__main__":
    try:
        n = int(input("请输入初始总人数 n: "))
        k = int(input("请输入报数临界值 k: "))
        
        if n <= 0 or k <= 0:
            print("输入错误：必须输入正整数。")
        else:
            print(f"切片法最后留下的是: {josephus_slice(n, k)} 号")
            print(f"迭代器法最后留下的是: {josephus_itertools(n, k)} 号")
            
    except ValueError:
        print("输入错误：请输入有效的数字。")