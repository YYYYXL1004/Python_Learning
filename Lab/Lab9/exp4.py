import csv
import datetime
import random
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# 设置中文字体，避免图形标题、坐标轴和图例文字无法正常显示。
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "KaiTi",
    "FangSong",
]
plt.rcParams["axes.unicode_minus"] = False


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "exp4_files"
DATA_FILE = OUTPUT_DIR / "data.csv"
FIRST_IMAGE = OUTPUT_DIR / "first.jpg"
SECOND_IMAGE = OUTPUT_DIR / "second.jpg"
THIRD_IMAGE = OUTPUT_DIR / "third.jpg"
MAX_MONTH_FILE = OUTPUT_DIR / "maxMonth.txt"


def make_data_csv():
    """生成饭店 2017 年每天营业额模拟数据。"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(9)

    with open(DATA_FILE, "w", newline="", encoding="utf-8-sig") as fp:
        wr = csv.writer(fp, lineterminator="\n")
        wr.writerow(["日期", "销量"])

        start_date = datetime.date(2017, 1, 1)
        for i in range(365):
            amount = 300 + i * 5 + random.randrange(100)
            wr.writerow([str(start_date), amount])
            start_date = start_date + datetime.timedelta(days=1)


def load_data():
    """读取 CSV 数据并删除缺失值。"""
    data = pd.read_csv(DATA_FILE)
    data = data.dropna()
    data["日期"] = pd.to_datetime(data["日期"])
    data["销量"] = pd.to_numeric(data["销量"], errors="coerce")
    data = data.dropna()
    data["月份"] = data["日期"].dt.month
    data["季度"] = data["日期"].dt.quarter
    return data


def draw_daily_line(data):
    """绘制每天营业额折线图。"""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(data["日期"], data["销量"], color="tab:blue", linewidth=1.5)
    ax.set_title("饭店每天营业额情况")
    ax.set_xlabel("日期")
    ax.set_ylabel("营业额")
    ax.grid(True, linestyle=":", alpha=0.6)

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig(FIRST_IMAGE, dpi=150)
    plt.close(fig)


def get_month_data(data):
    """按月份统计营业额总和。"""
    return data.groupby("月份")["销量"].sum()


def draw_month_bar(month_data):
    """绘制每月营业额柱状图。"""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(month_data.index.astype(str), month_data.values, color="tab:orange")
    ax.set_title("2017 年每月营业额")
    ax.set_xlabel("月份")
    ax.set_ylabel("营业额")
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.savefig(SECOND_IMAGE, dpi=150)
    plt.close(fig)


def save_max_month(month_data):
    """找出相邻月份中营业额涨幅最大的月份并写入文本文件。"""
    increase = month_data.diff()
    max_month = int(increase.idxmax())
    previous_month = max_month - 1
    max_value = int(increase.loc[max_month])

    with open(MAX_MONTH_FILE, "w", encoding="utf-8") as fp:
        fp.write(f"涨幅最大的月份：{max_month}月\n")
        fp.write(f"相邻月份：{previous_month}月 -> {max_month}月\n")
        fp.write(f"营业额涨幅：{max_value}\n")


def draw_quarter_pie(data):
    """绘制 2017 年四个季度营业额分布饼图。"""
    quarter_data = data.groupby("季度")["销量"].sum()
    labels = [f"第{quarter}季度" for quarter in quarter_data.index]

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        quarter_data.values,
        labels=labels,
        autopct="%.1f%%",
        startangle=90,
        counterclock=False,
    )
    ax.set_title("2017 年各季度营业额分布")

    plt.tight_layout()
    plt.savefig(THIRD_IMAGE, dpi=150)
    plt.close(fig)


def main():
    make_data_csv()
    data = load_data()
    month_data = get_month_data(data)

    draw_daily_line(data)
    draw_month_bar(month_data)
    save_max_month(month_data)
    draw_quarter_pie(data)

    print(f"文件已生成到：{OUTPUT_DIR}")


if __name__ == "__main__":
    main()
