from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 设置中文字体，避免标题、坐标轴和热力图标注无法正常显示。
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "KaiTi",
    "FangSong",
]
plt.rcParams["axes.unicode_minus"] = False


BASE_DIR = Path(__file__).resolve().parent
EXCEL_FILE = BASE_DIR / "exp3_files" / "学生成绩.xlsx"


def find_student_no_column(df):
    """优先查找学号列，找不到时使用第一列作为学生序号来源。"""
    for col in df.columns:
        if "学号" in str(col):
            return col

    return df.columns[0]


def find_score_column(df):
    """优先查找成绩列，找不到时选择最后一个可转换为数值的列。"""
    for col in df.columns:
        name = str(col)
        if "成绩" in name or "分数" in name:
            return col

    numeric_cols = []
    for col in df.columns:
        scores = pd.to_numeric(df[col], errors="coerce")
        if scores.notna().sum() > 0:
            numeric_cols.append(col)

    if not numeric_cols:
        raise ValueError("没有找到可用于绘图的成绩列。")

    return numeric_cols[-1]


def get_student_index(value, default_index):
    """取学号最后两位作为横轴编号，无法提取时使用原始顺序编号。"""
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    if len(digits) >= 2:
        return int(digits[-2:])

    return default_index


def load_score_data(excel_file):
    """读取所有工作表，将每个工作表整理为一个班级的成绩数据。"""
    sheets = pd.read_excel(excel_file, sheet_name=None)
    result = []

    for class_name, df in sheets.items():
        df = df.dropna(how="all")
        if df.empty:
            continue

        student_col = find_student_no_column(df)
        score_col = find_score_column(df)

        scores = pd.to_numeric(df[score_col], errors="coerce")
        temp = pd.DataFrame({
            "班级": class_name,
            "序号": [
                get_student_index(value, i + 1)
                for i, value in enumerate(df[student_col])
            ],
            "成绩": scores,
        })
        temp = temp.dropna(subset=["成绩"])
        result.append(temp)

    if not result:
        raise ValueError("Excel 文件中没有可用的成绩数据。")

    data = pd.concat(result, ignore_index=True)
    return data.sort_values(["班级", "序号"])


def draw_bar_chart(ax, data):
    """绘制不同班级相同学号后两位学生成绩的柱状图。"""
    sns.barplot(
        data=data,
        x="序号",
        y="成绩",
        hue="班级",
        ax=ax,
    )
    ax.set_title("两个班级学生成绩柱状图")
    ax.set_xlabel("学号后两位")
    ax.set_ylabel("成绩")
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=90)
    ax.grid(axis="y", linestyle=":", alpha=0.5)


def draw_heatmap(ax, data):
    """绘制班级和学号后两位对应成绩的热力图。"""
    table = data.pivot_table(
        index="班级",
        columns="序号",
        values="成绩",
        aggfunc="mean",
    )
    sns.heatmap(
        table,
        annot=True,
        fmt=".0f",
        cmap="YlOrRd",
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "成绩"},
        ax=ax,
    )
    ax.set_title("两个班级学生成绩热力图")
    ax.set_xlabel("学号后两位")
    ax.set_ylabel("班级")


def main():
    if not EXCEL_FILE.exists():
        print(f"没有找到文件：{EXCEL_FILE}")
        print("请将“学生成绩.xlsx”放到 Lab9/exp3_files 文件夹后重新运行。")
        return

    data = load_score_data(EXCEL_FILE)

    fig, axes = plt.subplots(2, 1, figsize=(12, 9))
    draw_bar_chart(axes[0], data)
    draw_heatmap(axes[1], data)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
