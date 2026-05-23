import os
import socket
import sys


# 默认服务端端口，需与exp3_ftpServer.py保持一致
PORT = 9002
# 网络通信使用的字符编码
ENCODING = "utf-8"
# 文件传输使用的缓冲区大小
BUFFER_SIZE = 4096
# 下载到本地的目录
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "exp3_ftp_download")


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


def recv_exact(sock, size):
    """从套接字中读取指定字节数的二进制数据。"""
    buf = bytearray()

    while len(buf) < size:
        chunk = sock.recv(min(BUFFER_SIZE, size - len(buf)))
        if not chunk:
            break
        buf.extend(chunk)

    return bytes(buf)


def do_login(sock):
    """登录服务端，返回是否登录成功。"""
    print("请输入用户名和密码进行登录（输入quit可退出）：")

    while True:
        username = input("用户名：").strip()
        if username.lower() in ("quit", "exit"):
            send_line(sock, "QUIT")
            return False
        if not username:
            continue

        password = input("密码：").strip()

        send_line(sock, f"LOGIN {username} {password}")
        response = recv_line(sock)
        if response is None:
            print("服务端已关闭连接。")
            return False

        print(response)
        if response.startswith("OK"):
            return True


def do_pwd(sock):
    """发送PWD命令并显示当前目录。"""
    send_line(sock, "PWD")
    response = recv_line(sock)
    if response and response.startswith("OK"):
        print(f"当前目录：{response[3:].strip()}")
    else:
        print(response)


def do_ls(sock):
    """发送LS命令并显示目录中文件列表。"""
    send_line(sock, "LS")
    response = recv_line(sock)
    if response is None or not response.startswith("OK"):
        print(response)
        return

    try:
        count = int(response.split(maxsplit=1)[1])
    except (IndexError, ValueError):
        print("服务端返回的数据格式错误。")
        return

    if count == 0:
        print("（当前目录为空）")
        return

    print(f"共{count}项：")
    for _ in range(count):
        line = recv_line(sock)
        if line is None:
            break
        print("  " + line)


def do_cd(sock, path):
    """发送CD命令切换目录。"""
    if not path:
        print("用法：cd <目录>")
        return

    send_line(sock, f"CD {path}")
    response = recv_line(sock)
    if response and response.startswith("OK"):
        print(f"已切换到：{response[3:].strip()}")
    else:
        print(response)


def do_get(sock, filename):
    """发送GET命令并下载文件到本地DOWNLOAD_DIR。"""
    if not filename:
        print("用法：get <文件名>")
        return

    send_line(sock, f"GET {filename}")
    response = recv_line(sock)
    if response is None or not response.startswith("OK"):
        print(response)
        return

    try:
        size = int(response.split(maxsplit=1)[1])
    except (IndexError, ValueError):
        print("服务端返回的数据格式错误。")
        return

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    save_name = os.path.basename(filename)
    save_path = os.path.join(DOWNLOAD_DIR, save_name)

    # 按服务端给出的字节数读取文件内容并写入本地文件
    data = recv_exact(sock, size)
    with open(save_path, "wb") as f:
        f.write(data)

    print(f"文件下载成功：{save_path}（{size}字节）")


def do_help():
    """显示帮助信息。"""
    print("可用命令：")
    print("  pwd            查看当前所在目录")
    print("  ls / dir       查看当前目录中的文件列表")
    print("  cd <目录>      切换到指定目录（支持 .. 返回上级）")
    print("  get <文件>     下载指定文件到本地")
    print("  help / ?       显示此帮助")
    print("  quit / exit    退出客户端")


def run_client(server_ip):
    """启动FTP模拟客户端，与服务端进行交互。"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((server_ip, PORT))
    except (ConnectionRefusedError, OSError) as e:
        print(f"无法连接到服务端 {server_ip}:{PORT}：{e}")
        return

    print(f"已连接到FTP服务端 {server_ip}:{PORT}")

    try:
        if not do_login(sock):
            return

        do_help()

        while True:
            try:
                line = input("\nftp> ").strip()
            except EOFError:
                break

            if not line:
                continue

            parts = line.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1].strip() if len(parts) > 1 else ""

            if cmd == "pwd":
                do_pwd(sock)
            elif cmd in ("ls", "dir"):
                do_ls(sock)
            elif cmd == "cd":
                do_cd(sock, arg)
            elif cmd == "get":
                do_get(sock, arg)
            elif cmd in ("help", "?"):
                do_help()
            elif cmd in ("quit", "exit", "bye"):
                send_line(sock, "QUIT")
                response = recv_line(sock)
                print(response or "已断开。")
                break
            else:
                print(f"未知命令：{cmd}，输入help查看帮助。")
    except (ConnectionResetError, KeyboardInterrupt):
        print("\n连接已断开。")
    finally:
        sock.close()


def main():
    # 服务端IP通过命令行参数传入，默认连接本机
    if len(sys.argv) >= 2:
        server_ip = sys.argv[1]
    else:
        server_ip = "127.0.0.1"
        print(f"未指定服务端IP，默认连接 {server_ip}")
        print("用法示例：python exp3_ftpClient.py 127.0.0.1\n")

    run_client(server_ip)


if __name__ == "__main__":
    main()
