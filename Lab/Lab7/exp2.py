import socket
import sys
import threading
from difflib import SequenceMatcher


# 服务端监听地址和端口
HOST = "127.0.0.1"
PORT = 9001
# 网络通信使用的字符编码
ENCODING = "utf-8"
# 客户端输入这些命令时主动退出
EXIT_WORDS = {"exit", "quit", "bye", "再见", "退出"}

# 服务端的"知识库"，键是问题，值是答案
QA_DATABASE = {
    "你是谁": "我是一个用Python编写的智能聊天机器人。",
    "你叫什么名字": "我叫小Py，很高兴认识你！",
    "你几岁了": "我今年刚刚诞生，还很年轻哦。",
    "Python是什么": "Python是一种简单易学、功能强大的高级编程语言。",
    "Python有什么特点": "Python语法简洁、跨平台、生态丰富，特别适合自动化和数据分析。",
    "如何学习Python": "建议先看官方教程，然后动手做小项目，多写多练效果最好。",
    "怎么安装Python": "可以到python.org下载安装包，安装时记得勾选Add to PATH。",
    "今天天气怎么样": "我还没有联网能力，建议你打开天气APP查看。",
    "你会做什么": "我会聊聊天，也能回答一些关于Python的小问题。",
    "你喜欢什么颜色": "我喜欢蓝色，因为它让我想起了Python的标志。",
    "这是lab7的第二个实验吗": "是的，你正在运行Lab7的第二个实验，体验一下简单的聊天机器人吧！",
    "你好": "你好！有什么我可以帮你的吗？",
    "在吗": "在的，有什么我可以帮你的吗？",
    "byebye": "再见，期待下次和你聊天！"
}


def find_best_answer(question):
    """根据用户输入，在知识库中查找最匹配的问题并返回答案。"""
    question = question.strip()
    if not question:
        return "你好像什么都没说哦。"

    # 1. 完全匹配，直接返回答案
    if question in QA_DATABASE:
        return QA_DATABASE[question]

    # 2. 输入是知识库中某个问题的子串，或某个问题是输入的子串
    sub_matches = [
        key for key in QA_DATABASE
        if question in key or key in question
    ]
    if sub_matches:
        # 取长度最相近的那一个，体现"识别真正想问的问题"
        best = min(sub_matches, key=lambda k: abs(len(k) - len(question)))
        return QA_DATABASE[best]

    # 3. 使用difflib计算相似度，找到分数最高的问题
    best_key = None
    best_score = 0.0

    for key in QA_DATABASE:
        score = SequenceMatcher(None, question, key).ratio()
        if score > best_score:
            best_score = score
            best_key = key

    # 相似度足够高才认为是匹配
    if best_key is not None and best_score >= 0.4:
        return f"你是想问 “{best_key}” 吗？\n{QA_DATABASE[best_key]}"

    return "抱歉，我还不会回答这个问题。"


def handle_client(conn, addr):
    """服务端处理单个客户端的会话。"""
    print(f"[连接] 客户端 {addr} 已上线。")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            question = data.decode(ENCODING).strip()
            print(f"[{addr}] 提问：{question}")

            # 客户端发送退出关键词时，回送告别并关闭连接
            if question.lower() in EXIT_WORDS:
                conn.sendall("再见！".encode(ENCODING))
                break

            answer = find_best_answer(question)
            conn.sendall(answer.encode(ENCODING))
    except ConnectionResetError:
        print(f"[断开] 客户端 {addr} 强制关闭了连接。")
    finally:
        conn.close()
        print(f"[断开] 客户端 {addr} 已离线。")


def run_server():
    """启动聊天服务端，循环监听客户端连接。"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"服务端已启动，正在监听 {HOST}:{PORT} ...")
    print("按 Ctrl+C 可以关闭服务端。\n")

    try:
        while True:
            conn, addr = server.accept()
            # 每个客户端用一个独立线程处理，支持多人同时聊天
            t = threading.Thread(target=handle_client,
                                 args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n服务端已关闭。")
    finally:
        server.close()


def run_client():
    """启动聊天客户端，向服务端发送问题并显示答案。"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"无法连接到服务端 {HOST}:{PORT}，请先启动服务端。")
        return

    print(f"已连接到聊天服务端 {HOST}:{PORT}")
    print("输入问题后回车提问，输入exit/quit/再见可以退出。\n")

    try:
        while True:
            question = input("我：").strip()
            if not question:
                continue

            client.sendall(question.encode(ENCODING))

            data = client.recv(2048)
            if not data:
                print("服务端已关闭连接。")
                break

            answer = data.decode(ENCODING)
            print(f"机器人：{answer}\n")

            if question.lower() in EXIT_WORDS:
                break
    except (ConnectionResetError, KeyboardInterrupt):
        print("\n聊天已结束。")
    finally:
        client.close()


def main():
    # 通过命令行参数决定运行服务端还是客户端
    if len(sys.argv) < 2:
        print("用法：")
        print("  启动服务端：python exp2.py server")
        print("  启动客户端：python exp2.py client")
        return

    mode = sys.argv[1].lower()
    if mode == "server":
        run_server()
    elif mode == "client":
        run_client()
    else:
        print(f"未知模式：{mode}，请使用 server 或 client。")


if __name__ == "__main__":
    main()
