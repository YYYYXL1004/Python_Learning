import os
import re

from PIL import Image, ImageDraw, ImageFont


# 保存图片和HTML文件的文件夹
SAVE_DIR = os.path.join(os.path.dirname(__file__), "exp1_files")
IMAGE_DIR = os.path.join(SAVE_DIR, "images")
HTML_FILE = os.path.join(SAVE_DIR, "index.html")

# 用于生成测试用的幻灯片图片，模拟从PPT中导出
SLIDE_TITLES = [
    ("Python办公自动化", "课程介绍与目录"),
    ("第一章", "Excel文件读写"),
    ("第二章", "多文件合并与统计"),
    ("第三章", "Word文档生成"),
    ("第四章", "Word文本处理"),
    ("第五章", "PPT幻灯片自动生成"),
    ("第六章", "PPT表格读取"),
    ("第七章", "HTML网页批量制作"),
    ("第八章", "综合实战项目"),
    ("课程小结", "感谢观看，再见！")
]
# 不同幻灯片使用不同背景颜色，让旋转效果更明显
SLIDE_COLORS = [
    (52, 73, 94), (231, 76, 60), (243, 156, 18), (39, 174, 96),
    (41, 128, 185), (142, 68, 173), (22, 160, 133), (211, 84, 0),
    (44, 62, 80), (192, 57, 43)
]


def load_chinese_font(size):
    """加载本机中文字体，找不到时退回到默认字体。"""
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc"
    ]

    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def make_test_images():
    """生成模拟从PPT中导出的多张幻灯片图片。"""
    os.makedirs(IMAGE_DIR, exist_ok=True)

    title_font = load_chinese_font(64)
    subtitle_font = load_chinese_font(36)
    page_font = load_chinese_font(24)

    width, height = 960, 720

    for i, (title, subtitle) in enumerate(SLIDE_TITLES, 1):
        bg_color = SLIDE_COLORS[(i - 1) % len(SLIDE_COLORS)]
        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # 在底部画一条装饰横条，让图片看起来更像幻灯片
        draw.rectangle([0, height - 60, width, height], fill=(255, 255, 255))

        # 居中绘制主标题
        bbox = draw.textbbox((0, 0), title, font=title_font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((width - tw) / 2, height / 2 - th - 20), title,
                  fill="white", font=title_font)

        # 居中绘制副标题
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((width - sw) / 2, height / 2 + 20), subtitle,
                  fill="white", font=subtitle_font)

        # 右下角显示页码
        page_text = f"{i} / {len(SLIDE_TITLES)}"
        draw.text((width - 110, height - 45), page_text,
                  fill=bg_color, font=page_font)

        # 文件名补零，方便后续按字符串排序时也能保持顺序
        img.save(os.path.join(IMAGE_DIR, f"slide_{i:02d}.png"))


def get_image_files():
    """获取图片文件夹中所有图片，按文件名中的序号升序排列。"""
    if not os.path.exists(IMAGE_DIR):
        return []

    exts = (".png", ".jpg", ".jpeg", ".gif", ".bmp")
    files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(exts)]

    # 通过正则提取文件名中的数字，按数字大小排序
    def sort_key(name):
        m = re.search(r"(\d+)", name)
        return int(m.group(1)) if m else 0

    files.sort(key=sort_key)
    return files


def make_html_page():
    """读取图片文件夹中的所有图片，按序号升序生成HTML5网页。"""
    files = get_image_files()

    if not files:
        print("没有找到图片文件，请先准备图片。")
        return

    # 使用列表推导式生成所有<img>标签
    img_tags = [
        f'        <img src="images/{name}" alt="第{i}张幻灯片">'
        for i, name in enumerate(files, 1)
    ]

    # HTML5模板：利用nth-child为不同位置的图片设置不同旋转角度
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>幻灯片图片展示</title>
    <style>
        body {{
            background: #f5f5f0;
            margin: 0;
            padding: 30px;
            font-family: "Microsoft YaHei", sans-serif;
        }}
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }}
        .gallery {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
        }}
        .gallery img {{
            width: 280px;
            margin: 25px;
            background: #fff;
            padding: 8px;
            border: 1px solid #ddd;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
            transition: transform 0.4s ease;
        }}
        .gallery img:nth-child(4n+1) {{ transform: rotate(-6deg); }}
        .gallery img:nth-child(4n+2) {{ transform: rotate(3deg); }}
        .gallery img:nth-child(4n+3) {{ transform: rotate(-2deg); }}
        .gallery img:nth-child(4n)   {{ transform: rotate(7deg); }}
        /* 鼠标悬停时放大并恢复正向，方便查看细节 */
        .gallery img:hover {{
            transform: scale(1.15) rotate(0deg);
            z-index: 10;
        }}
    </style>
</head>
<body>
    <h1>幻灯片图片展示（共{len(files)}张）</h1>
    <div class="gallery">
{chr(10).join(img_tags)}
    </div>
</body>
</html>
"""

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"共导入{len(files)}张图片，HTML文件已保存到：{HTML_FILE}")


def main():
    # 没有图片时，先生成一组模拟幻灯片图片用于测试
    if not os.path.exists(IMAGE_DIR) or not get_image_files():
        make_test_images()

    make_html_page()


if __name__ == "__main__":
    main()
