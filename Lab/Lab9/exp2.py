import numpy as np
import matplotlib.pyplot as plt


# 设置中文字体，避免标题、坐标轴和标注文字无法正常显示。
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "KaiTi",
    "FangSong",
]
plt.rcParams["axes.unicode_minus"] = False


POINT_DISTANCE = 2


def get_nearest_point(ax, x_data, y_data, event):
    """计算鼠标到正弦曲线折线段的最小屏幕像素距离。"""
    points = np.column_stack((x_data, y_data))
    screen_points = ax.transData.transform(points)

    start_points = screen_points[:-1]
    end_points = screen_points[1:]
    segment_vectors = end_points - start_points
    mouse_point = np.array([event.x, event.y])

    mouse_vectors = mouse_point - start_points
    segment_lengths = np.sum(segment_vectors ** 2, axis=1)
    ratios = np.sum(mouse_vectors * segment_vectors, axis=1) / segment_lengths
    ratios = np.clip(ratios, 0, 1)

    nearest_points = start_points + segment_vectors * ratios[:, None]
    distances = np.hypot(nearest_points[:, 0] - event.x, nearest_points[:, 1] - event.y)
    index = np.argmin(distances)

    x = x_data[index] + ratios[index] * (x_data[index + 1] - x_data[index])
    y = y_data[index] + ratios[index] * (y_data[index + 1] - y_data[index])

    return distances[index], x, y


def main():
    x_data = np.linspace(0, 2 * np.pi, 600)
    y_data = np.sin(x_data)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_data, y_data, color="tab:blue", linewidth=2)

    ax.set_title("一个周期的正弦曲线")
    ax.set_xlabel("x")
    ax.set_ylabel("sin(x)")
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1.2, 1.2)
    ax.grid(True, linestyle=":", alpha=0.6)

    # 文本标注默认隐藏，鼠标靠近曲线时再显示当前坐标值。
    annotation = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(0, 18),
        textcoords="offset points",
        ha="center",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9),
        arrowprops=dict(arrowstyle="->", color="gray"),
    )
    annotation.set_visible(False)

    def enter_axes(event):
        if event.inaxes == ax:
            ax.set_facecolor("yellow")
            fig.canvas.draw_idle()

    def leave_axes(event):
        if event.inaxes == ax:
            ax.set_facecolor("white")
            annotation.set_visible(False)
            fig.canvas.draw_idle()

    def move_mouse(event):
        if event.inaxes != ax:
            if annotation.get_visible():
                annotation.set_visible(False)
                fig.canvas.draw_idle()
            return

        distance, x, y = get_nearest_point(ax, x_data, y_data, event)
        if distance < POINT_DISTANCE:
            annotation.xy = (x, y)
            annotation.set_text(f"x={x:.2f}\ny={y:.2f}")
            annotation.set_visible(True)
        else:
            annotation.set_visible(False)

        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("axes_enter_event", enter_axes)
    fig.canvas.mpl_connect("axes_leave_event", leave_axes)
    fig.canvas.mpl_connect("motion_notify_event", move_mouse)

    plt.show()


if __name__ == "__main__":
    main()
