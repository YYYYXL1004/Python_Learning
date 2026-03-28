def cni(n, i): 
    minNI = min(i, n-i)
    result = 1
    for j in range(0, minNI) :
        # 使用 // 保持整数类型，避免浮点数精度丢失
        result = result * (n - j) // (j + 1)
    return result

print(f"cni(5, 2) = {cni(5, 2)}")
print(f"cni(10, 3) = {cni(10, 3)}")
print(f"cni(20, 10) = {cni(20, 10)}")
print(f"cni(6, 0) = {cni(6, 0)}")
print(f"cni(6, 6) = {cni(6, 6)}")
print(f"cni(100, 50) = {cni(100, 50)}")
