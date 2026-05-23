import os
import socket
import threading


# 服务端监听地址和端口
HOST = "0.0.0.0"
PORT = 9002
# 网络通信使用的字符编码
ENCODING = "utf-8"
# 文件传输使用的缓冲区大小
BUFFER_SIZE = 4096

# 共享文件的根目录，所有客户端只能访问这个目录内的文件
ROOT_DIR = os.path.join(os.path.dirname(__file__), "exp3_ftp_root")
# 简单的用户名/密码字典，模拟登录验证
USERS = {
    "admin": "123456",
    "guest": "guest"
}


def make_test_files():
    """生成一些用于测试的目录和文件。"""
    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)

    samples = {
        "readme.txt": "欢迎使用Python模拟FTP服务器！\n支持的命令：pwd、ls、cd、get、quit。\n",
        "hello.txt": "Hello, FTP World!\n",
        "docs/intro.txt": "这是docs子目录下的一个文本文件。\n",
        "docs/python.txt": "Python是一种优秀的编程语言。\n",
        "images/note.txt": "这里假装是图片目录。\n"
    }

    for rel_path, content in samples.items():
        full_path = os.path.join(ROOT_DIR, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if not os.path.exists(full_path):
            with open(full_path, "w", encoding=ENCODING) as f:
                f.write(content)


def recv_line(sock):
    """从套接字中接收一行文本，以\\n结尾。"""
    buf = bytearray()

    while True:
        ch = sock.recv(1)
        if not ch:
            return None
        if ch == b"\n":
            return buf.decode(ENCODING, errors="replace").rstrip("\r")
        buf.extend(ch)


def send_line(sock, text):
    """向套接字发送一行文本，自动追加\\n。"""
    sock.sendall((text + "\n").encode(ENCODING))


def safe_resolve(cwd, path):
    """把客户端给出的路径解析为绝对路径，并确保不超出根目录。"""
    # 支持绝对路径（相对ROOT_DIR）和相对路径
    if path.startswith("/") or path.startswith("\\"):
        target = os.path.join(ROOT_DIR, path.lstrip("/\\"))
    else:
        target = os.path.join(cwd, path)

    target = os.path.realpath(target)
    root = os.path.realpath(ROOT_DIR)

    # 不允许通过 ../ 跳到 ROOT_DIR 之外
    if target != root and not target.startswith(root + os.sep):
        return None
    return target


def relative_path(path):
    """把绝对路径转换为相对于ROOT_DIR的显示路径。"""
    rel = os.path.relpath(path, ROOT_DIR)
    if rel == ".":
        return "/"
    # 在网络协议中统一使用正斜杠，避免不同操作系统的差异
    return "/" + rel.replace(os.sep, "/")


def handle_login(conn):
    """处理客户端的登录请求，返回登录成功的用户名。"""
    while True:
        line = recv_line(conn)
        if line is None:
            return None

        parts = line.split(maxsplit=2)
        if len(parts) >= 1 and parts[0].upper() == "QUIT":
            send_line(conn, "BYE")
            return None

        if len(parts) < 3 or parts[0].upper() != "LOGIN":
            send_line(conn, "ERR 请使用 LOGIN <用户名> <密码> 登录")
            continue

        username, password = parts[1], parts[2]
        if USERS.get(username) == password:
            send_line(conn, f"OK 欢迎你，{username}")
            return username

        send_line(conn, "ERR 用户名或密码错误")


def cmd_pwd(conn, cwd):
    """处理PWD命令：返回当前目录。"""
    send_line(conn, f"OK {relative_path(cwd)}")


def cmd_ls(conn, cwd):
    """处理LS命令：返回当前目录下的文件和子目录列表。"""
    try:
        entries = sorted(os.listdir(cwd))
    except OSError as e:
        send_line(conn, f"ERR 无法列出目录：{e}")
        return

    # 先发送条目数量，再逐行发送条目名称，目录在名字后面加 /
    send_line(conn, f"OK {len(entries)}")

    for name in entries:
        full = os.path.join(cwd, name)
        if os.path.isdir(full):
            send_line(conn, name + "/")
        else:
            size = os.path.getsize(full)
            send_line(conn, f"{name}\t{size}B")


def cmd_cd(conn, cwd, arg):
    """处理CD命令：切换目录，返回新的当前目录。"""
    if not arg:
        send_line(conn, "ERR 用法：cd <目录>")
        return cwd

    target = safe_resolve(cwd, arg)
    if target is None or not os.path.exists(target):
        send_line(conn, "ERR 目录不存在或越界")
        return cwd
    if not os.path.isdir(target):
        send_line(conn, "ERR 这不是一个目录")
        return cwd

    send_line(conn, f"OK {relative_path(target)}")
    return target


def cmd_get(conn, cwd, arg):
    """处理GET命令：把文件二进制内容发送给客户端。"""
    if not arg:
        send_line(conn, "ERR 用法：get <文件名>")
        return

    target = safe_resolve(cwd, arg)
    if target is None or not os.path.exists(target):
        send_line(conn, "ERR 文件不存在或越界")
        return
    if not os.path.isfile(target):
        send_line(conn, "ERR 这不是一个文件")
        return

    size = os.path.getsize(target)
    # 先发送OK和文件大小，客户端据此读取后续的二进制数据
    send_line(conn, f"OK {size}")

    with open(target, "rb") as f:
        while True:
            chunk = f.read(BUFFER_SIZE)
            if not chunk:
                break
            conn.sendall(chunk)


def handle_client(conn, addr):
    """与单个客户端的完整会话流程。"""
    print(f"[连接] 客户端 {addr} 已连接。")

    try:
        username = handle_login(conn)
        if username is None:
            return

        cwd = ROOT_DIR
        print(f"[登录] 用户 {username} 来自 {addr} 登录成功。")

        while True:
            line = recv_line(conn)
            if line is None:
                break

            parts = line.split(maxsplit=1)
            if not parts:
                continue

            cmd = parts[0].upper()
            arg = parts[1].strip() if len(parts) > 1 else ""
            print(f"[{username}@{addr[0]}] {cmd} {arg}")

            if cmd == "PWD":
                cmd_pwd(conn, cwd)
            elif cmd == "LS" or cmd == "DIR":
                cmd_ls(conn, cwd)
            elif cmd == "CD":
                cwd = cmd_cd(conn, cwd, arg)
            elif cmd == "GET":
                cmd_get(conn, cwd, arg)
            elif cmd == "QUIT":
                send_line(conn, "BYE")
                break
            else:
                send_line(conn, f"ERR 未知命令：{cmd}")
    except ConnectionResetError:
        print(f"[断开] 客户端 {addr} 强制关闭了连接。")
    finally:
        conn.close()
        print(f"[断开] 客户端 {addr} 已离线。\n")


def run_server():
    """启动FTP模拟服务端。"""
    make_test_files()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"FTP服务端已启动，监听 {HOST}:{PORT}")
    print(f"共享根目录：{ROOT_DIR}")
    print("可用用户：" + "、".join(f"{u}/{p}" for u, p in USERS.items()))
    print("按 Ctrl+C 关闭服务端。\n")

    try:
        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client,
                                 args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n服务端已关闭。")
    finally:
        server.close()


def main():
    run_server()


if __name__ == "__main__":
    main()
