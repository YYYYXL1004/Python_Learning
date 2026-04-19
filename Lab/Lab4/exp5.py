def hanoi(n, source='A', target='C', temp='B', pegs=None):
    """
    递归解决汉诺塔问题并打印每步底座状态。
    """
    if pegs is None:
        pegs = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}
        print(f"初始状态: A: {pegs['A']} | B: {pegs['B']} | C: {pegs['C']}\n")

    if n == 1:
        disk = pegs[source].pop()
        pegs[target].append(disk)
        # 修复：先将列表转为 str，再使用 :<15 进行左对齐，保证输出整齐
        print(f"移动盘子 {disk}: {source} -> {target}\t| 状态: A: {str(pegs['A']):<15} B: {str(pegs['B']):<15} C: {pegs['C']}")
    else:
        hanoi(n - 1, source, temp, target, pegs)
        
        disk = pegs[source].pop()
        pegs[target].append(disk)
        # 修复：同上
        print(f"移动盘子 {disk}: {source} -> {target}\t| 状态: A: {str(pegs['A']):<15} B: {str(pegs['B']):<15} C: {pegs['C']}")
        
        hanoi(n - 1, temp, target, source, pegs)

if __name__ == "__main__":
    try:
        n = int(input("请输入盘子数量 n: "))
        
        if n <= 0:
            print("输入错误：盘子数量必须是正整数。")
        elif n > 8:
            print("警告：盘子数量大于8会导致输出极长，建议输入小一点的数字以观察过程。")
        else:
            print("\n=== 汉诺塔移动过程模拟 ===")
            hanoi(n)
            
    except ValueError:
        print("输入错误：请输入有效的整数。")