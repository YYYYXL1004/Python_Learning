import os
import hashlib

def main():
    file_path = input("请输入要计算MD5的文件名：")

    # 判断文件是否存在
    if not os.path.exists(file_path): 
        print(f"文件{file_path}不存在，请检查路径！")
        return 
    
    # 初始化一个MD5哈希对象
    md5_obj = hashlib.md5()

    # 这里必须是'rb'，以二进制模式读取，因为MD5计算依赖于底层的Bytes而不是字符
    with open(file_path, 'rb') as f:
        # 文件比较小直接f.read()一次性读入内存就行
        # 如果是几个G的大文件，通常使用while搭配 f.read(4090)分块读取防止OOM
        content = f.read()
        md5_obj.update(content)
    
    result = md5_obj.hexdigest()
    print(f"{file_path}的MD5值为：{result}")

if __name__ == "__main__":
    main()