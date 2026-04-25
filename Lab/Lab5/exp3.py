import os
import sys

TARGET_EXTS = ('.tmp', '.log', '.obj', '.txt')

def dfs_clean(cur_dir):
    # 使用dfs递归遍历并清理目录
    try:
        # 获取当前目录下的所有文件和子文件夹名称
        for item in os.listdir(cur_dir):
            # 拼接完整的路径
            item_path = os.path.join(cur_dir, item)

            # 如果是目录，递归遍历
            if os.path.isdir(item_path):
                dfs_clean(item_path)

            elif os.path.isfile(item_path):
                # str.endswith() 只要字符串以元祖中的任意元素结尾，都会返回True
                if item.lower().endswith(TARGET_EXTS) or os.path.getsize(item_path) == 0:
                    try: 
                        os.remove(item_path)
                        print(f"{item_path}已删除")
                    except Exception as e:
                        print(f"删除失败：{item_path}: {e}")
    except PermissionError:
        print(f"权限不足，无法访问目录: {cur_dir}")


if __name__ == "__main__":
    # sys.argv 是一个列表，存储命令行参数
    # sys.argv[0] 永远是脚本名本身， sys.argv[1]才是我们传入的第一个参数
    if len(sys.argv) < 2:
        print("请重新输入要清理的文件夹路径")
        sys.exit(1)  # 非0错误码表示程序异常退出

    target_path = sys.argv[1]

    if not os.path.isdir(target_path):
        print(f"{target_path} 不是一个有效的文件夹路径")
        sys.exit(1)

    print(f"=== 开始清理文件夹：{target_path} ===")
    dfs_clean(target_path)
    print(f"=== 清理完成 ===")