def task1(n):
    # 将整数 n 转换为字符串，遍历每个字符，将其转换回整数并求和
    return sum(int(char) for char in str(n))

print(f"task1(99999) = {task1(99999)}")

def task2(setA, setB):
    # A和B的交集
    intersection = setA & setB
    # A和B的并集
    union = setA | setB
    # A和B的差集
    difference = setA - setB
    return intersection, union, difference

setA = {1, 2, 3, 4, 5}
setB = {3, 4, 5, 6, 7}
intersection, union, difference = task2(setA, setB)
print(f"task2(setA = {setA}, setB = {setB}) = ", end="")
print(f"交集：{intersection}, 并集：{union}, 差集：{difference}")

def task3(n):
    # 将整数 n 转换为二进制、八进制和十六进制字符串
    return bin(n), oct(n), hex(n)

b, o, h = task3(255)
print(f"task3(255) = ", end="")
print(f"二进制：{b}, 八进制：{o}, 十六进制：{h}")

def task4(lst):
    # 使用filter函数返回列表中所有偶数
    # return list(filter(lambda x : x % 2 == 0, lst))
    # 使用列表推导式返回列表中所有偶数
    return [x for x in lst if x % 2 == 0]

print(f"task4([1, 2, 3, 4, 5, 6]) = {task4([1, 2, 3, 4, 5, 6])}")

def task5(lstA, lstB):
    # 使用zip函数将两个列表组合成一个字典
    return dict(zip(lstA, lstB))

lstA = [1, 2, 3]
lstB = [4, 5, 6]
print(f"task5({lstA}, {lstB}) = {task5(lstA, lstB)}")

def task6(lst):
    # 使用sorted函数对列表进行排序，reverse=True表示降序排序
    return sorted(lst, reverse=True)

print(f"task6([3, 1, 4, 1, 5, 9]) = {task6([3, 1, 4, 1, 5, 9])}")

import functools
def task7(lst):
    # 使用reduce函数计算列表中所有元素的积
    return functools.reduce(lambda x, y : x * y, lst)

print(f"task7([1, 2, 3, 4, 5]) = {task7([1, 2, 3, 4, 5])}")

def task8(a1, q, n):
    # 等比数列求和公式：S_n = a1 * (q^n - 1) / (q - 1)，其中a1是首项，q是公比，n是项数
    return int(a1 * (q ** n - 1) / (q - 1))

print(f"task8(1, 2, 10) = {task8(1, 2, 10)}")

def task9(s):
    cnt = {}
    for c in s:
        # 使用字典的get方法统计每个字符出现的次数，默认值为0
        cnt[c] = cnt.get(c, 0) + 1
        
    # 找出字典中 Value (值) 最大的 Key (键)    
    max_char = max(cnt, key=cnt.get)
    return max_char, cnt[max_char]

for s in ["hello", "aabbcc", "abcdefg", "aaabbbccccdd"]:
    char, count = task9(s)
    print(f'task9("{s}") = ', end="")
    print(f'输入: "{s}" -> 输出: {char} 出现 {count} 次')