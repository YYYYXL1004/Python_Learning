import time

import psutil


# 采样时间间隔（秒），每隔这么久统计一次流量
INTERVAL = 1


def format_size(num_bytes):
    """把字节数格式化为带单位的人类可读字符串。"""
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            # 使用字符串格式化，保留两位小数并右对齐
            return f"{size:8.2f} {unit}"
        size /= 1024
    return f"{size:8.2f} PB"


def get_net_bytes():
    """读取系统当前累计发送和接收的字节数。"""
    io = psutil.net_io_counters()
    return io.bytes_sent, io.bytes_recv


def monitor():
    """实时监控网络流量，输出上行/下行速度和累计流量。"""
    header = f"{'时间':<10}{'上行速度':>16}{'下行速度':>16}" \
             f"{'累计上行':>16}{'累计下行':>16}"
    print(header)
    print("-" * 74)

    prev = get_net_bytes()

    while True:
        time.sleep(INTERVAL)
        cur = get_net_bytes()

        # 用map配合lambda把(prev, cur)对应位置相减并除以采样间隔，得到字节/秒
        speeds = list(map(
            lambda pair: (pair[1] - pair[0]) / INTERVAL,
            zip(prev, cur)
        ))

        # 再用map配合lambda把速度字节数格式化成 "数值 单位/s"
        up_speed, down_speed = map(lambda x: format_size(x) + "/s", speeds)

        # 累计流量也用map统一格式化
        up_total, down_total = map(format_size, cur)

        timestamp = time.strftime("%H:%M:%S")
        print(f"{timestamp:<10}{up_speed:>16}{down_speed:>16}"
              f"{up_total:>16}{down_total:>16}")

        prev = cur


def main():
    print(f"网络流量监控启动（采样间隔 {INTERVAL} 秒），按 Ctrl+C 停止\n")

    try:
        monitor()
    except KeyboardInterrupt:
        print("\n监控已停止。")


if __name__ == "__main__":
    main()
