import math

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.widgets import Button, Slider


# 设置中文字体，避免标题、图例、按钮文字显示为方框或触发缺字警告。
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "KaiTi",
    "FangSong",
]
plt.rcParams["axes.unicode_minus"] = False


DEFAULT_SIDES = 6
MIN_SIDES = 3
MAX_SIDES = 60
RADIUS = 1


def make_polygon_points(sides):
    """根据边数生成外接于单位圆的正多边形顶点坐标。"""
    points = []
    start_angle = math.pi / 2

    for i in range(sides):
        angle = start_angle + 2 * math.pi * i / sides
        x = RADIUS * math.cos(angle)
        y = RADIUS * math.sin(angle)
        points.append((x, y))

    return points


def draw_polygon(ax, sides):
    """清空画布并重新绘制圆周和对应边数的正多边形。"""
    ax.clear()

    circle = Circle(
        (0, 0),
        RADIUS,
        fill=False,
        linestyle="--",
        linewidth=2,
        edgecolor="tab:blue",
        label="圆周",
    )
    polygon = Polygon(
        make_polygon_points(sides),
        closed=True,
        fill=False,
        linewidth=2,
        edgecolor="tab:red",
        label=f"正{sides}边形",
    )

    ax.add_patch(circle)
    ax.add_patch(polygon)
    ax.set_title(f"正{sides}边形逼近圆周")
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right")


def main():
    """创建带 Slider 和 Button 组件的交互式绘图窗口。"""
    fig, ax = plt.subplots(figsize=(7, 7))
    plt.subplots_adjust(bottom=0.22)

    draw_polygon(ax, DEFAULT_SIDES)

    # Slider 用来动态调整正多边形边数，取值为整数。
    slider_ax = fig.add_axes([0.18, 0.1, 0.58, 0.04])
    side_slider = Slider(
        slider_ax,
        "边数",
        MIN_SIDES,
        MAX_SIDES,
        valinit=DEFAULT_SIDES,
        valstep=1,
    )

    # Button 用来将 Slider 恢复为默认值。
    button_ax = fig.add_axes([0.8, 0.09, 0.12, 0.06])
    reset_button = Button(button_ax, "恢复默认")

    def update(value):
        sides = int(value)
        draw_polygon(ax, sides)
        fig.canvas.draw_idle()

    def reset(event):
        side_slider.reset()

    side_slider.on_changed(update)
    reset_button.on_clicked(reset)

    plt.show()


if __name__ == "__main__":
    main()
