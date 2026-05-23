import socket
import sys
import time


# 用于自动发现的广播端口，服务端和客户端必须一致
DISCOVERY_PORT = 9100
# 服务端广播的标识信息，客户端用它判断是否是自己关心的服务
DISCOVERY_MESSAGE = "ServerIP"
# 服务端广播的时间间隔（秒）
BROADCAST_INTERVAL = 1
# 网络通信使用的字符编码
ENCODING = "utf-8"


def get_local_ip():
    """获取本机在局域网中的IP地址。"""
    # 通过连接外部地址的方式让操作系统选择正确的网卡，不会真正发送数据
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        sock.close()
    return ip


def run_server():
    """服务端：每隔1秒向局域网广播一次ServerIP信息。"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 启用广播功能
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    local_ip = get_local_ip()
    # 在广播信息后面附上本机IP，客户端既能从消息中读取，也能从UDP包源地址读取
    data = f"{DISCOVERY_MESSAGE} {local_ip}".encode(ENCODING)

    print(f"自动发现服务已启动，本机IP：{local_ip}")
    print(f"正在向 255.255.255.255:{DISCOVERY_PORT} 广播信息...")
    print("按 Ctrl+C 可以停止广播。\n")

    count = 0
    try:
        while True:
            sock.sendto(data, ("255.255.255.255", DISCOVERY_PORT))
            count += 1
            print(f"[{count:>4}] 已广播：{DISCOVERY_MESSAGE} {local_ip}")
            time.sleep(BROADCAST_INTERVAL)
    except KeyboardInterrupt:
        print("\n广播已停止。")
    finally:
        sock.close()


def run_client():
    """客户端：监听广播信息，获取并输出服务端的IP地址。"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定到所有网卡的指定端口，接收来自任意主机的广播
    sock.bind(("", DISCOVERY_PORT))

    print(f"正在监听UDP {DISCOVERY_PORT}端口，等待服务端广播...")
    print("按 Ctrl+C 可以停止监听。\n")

    seen = set()

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            text = data.decode(ENCODING, errors="replace").strip()

            # 只关心携带ServerIP标识的广播包
            if not text.startswith(DISCOVERY_MESSAGE):
                continue

            # 源IP是从UDP包的发送方地址中直接获取的，最可靠
            server_ip = addr[0]

            # 同一个服务端IP第一次出现时打印详细信息，后续只打印心跳
            if server_ip not in seen:
                seen.add(server_ip)
                print(f"[发现] 找到服务端：{server_ip}")
                print(f"       完整消息：{text}\n")
            else:
                print(f"[心跳] {server_ip} 仍在线")
    except KeyboardInterrupt:
        print("\n监听已停止。")
    finally:
        sock.close()


def main():
    # 通过命令行参数决定运行服务端还是客户端
    if len(sys.argv) < 2:
        print("用法：")
        print("  启动服务端：python exp4.py server")
        print("  启动客户端：python exp4.py client")
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
