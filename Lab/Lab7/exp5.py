import os
import smtplib
import ssl
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from PIL import Image, ImageDraw, ImageFont


# === 发件人SMTP账号配置 ===
# 使用QQ邮箱时，PASSWORD填写"客户端授权码"而不是登录密码
# 使用163邮箱时，PASSWORD填写"客户端授权密码"
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
FROM_EMAIL = "your_email@qq.com"
FROM_NAME = "Python邮件群发测试"
PASSWORD = "your_smtp_auth_code"

# === 群发收件人列表 ===
RECIPIENTS = [
    "test1@example.com",
    "test2@example.com"
]

# 邮件主题和HTML正文，HTML正文中通过cid引用嵌入图片
SUBJECT = "来自Python的群发测试邮件"
HTML_TEMPLATE = """\
<html>
<body style="font-family: 'Microsoft YaHei', sans-serif;">
    <p>各位同学好：</p>
    <p>这是一封通过Python程序自动发送的<b>群发测试邮件</b>，正文中嵌入了图片，并且带有附件文件。</p>
    <p><img src="cid:image1" alt="嵌入图片"></p>
    <p>感谢阅读，祝学习愉快！</p>
    <p style="color:#888">—— Python办公自动化课程</p>
</body>
</html>
"""

# 测试用文件路径
SAVE_DIR = os.path.join(os.path.dirname(__file__), "exp5_files")
INLINE_IMAGE = os.path.join(SAVE_DIR, "inline.png")
ATTACHMENT_FILE = os.path.join(SAVE_DIR, "附件说明.txt")
PREVIEW_FILE = os.path.join(SAVE_DIR, "preview.eml")


def load_chinese_font(size):
    """加载本机中文字体，找不到时退回到默认字体。"""
    for path in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_test_files():
    """生成测试用的嵌入图片和附件文件。"""
    os.makedirs(SAVE_DIR, exist_ok=True)

    if not os.path.exists(INLINE_IMAGE):
        img = Image.new("RGB", (480, 200), color=(41, 128, 185))
        draw = ImageDraw.Draw(img)
        draw.text((30, 70), "Hello, Email!", fill="white",
                  font=load_chinese_font(40))
        img.save(INLINE_IMAGE)

    if not os.path.exists(ATTACHMENT_FILE):
        with open(ATTACHMENT_FILE, "w", encoding="utf-8") as f:
            f.write("这是一个测试附件文件。\n")
            f.write("用于演示Python发送电子邮件时附件的传输。\n")


def attach_inline_image(container, image_path, cid):
    """以inline方式把图片添加到邮件中，HTML中用 cid:<id> 引用。"""
    with open(image_path, "rb") as f:
        img = MIMEImage(f.read())

    # Content-ID用尖括号包裹，HTML中通过相同的id引用
    img.add_header("Content-ID", f"<{cid}>")
    img.add_header("Content-Disposition", "inline",
                   filename=os.path.basename(image_path))
    container.attach(img)


def attach_file(container, file_path):
    """以附件形式把文件添加到邮件中，支持中文文件名。"""
    with open(file_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    # 二进制内容用base64编码，是邮件附件的标准做法
    encoders.encode_base64(part)

    # 用RFC 2231规范的(charset, language, value)三元组写入文件名，避免中文乱码
    filename = os.path.basename(file_path)
    part.add_header("Content-Disposition", "attachment",
                    filename=("utf-8", "", filename))
    container.attach(part)


def build_email(recipient):
    """构造一封带嵌入图片和附件的MIME邮件。

    邮件结构：
        multipart/mixed                  # 顶层：正文 + 附件
        ├── multipart/related            # 内层：HTML正文 + 内嵌图片
        │   ├── text/html
        │   └── image/png (Content-ID)
        └── application/octet-stream     # 附件文件
    """
    msg = MIMEMultipart("mixed")
    msg["Subject"] = Header(SUBJECT, "utf-8")
    msg["From"] = formataddr((str(Header(FROM_NAME, "utf-8")), FROM_EMAIL))
    msg["To"] = recipient

    # 内层multipart/related，存放HTML正文和它引用的嵌入图片
    body = MIMEMultipart("related")
    msg.attach(body)

    # HTML正文部分
    html_part = MIMEText(HTML_TEMPLATE, "html", "utf-8")
    body.attach(html_part)

    # 嵌入图片，cid与HTML中保持一致
    if os.path.exists(INLINE_IMAGE):
        attach_inline_image(body, INLINE_IMAGE, "image1")

    # 附件文件
    if os.path.exists(ATTACHMENT_FILE):
        attach_file(msg, ATTACHMENT_FILE)

    return msg


def save_preview(msg):
    """把构造好的邮件以.eml格式保存到本地以便预览。"""
    with open(PREVIEW_FILE, "w", encoding="utf-8") as f:
        f.write(msg.as_string())
    print(f"邮件预览已保存：{PREVIEW_FILE}")
    print("可以用Outlook、Foxmail等邮件客户端打开.eml文件查看完整效果。")


def is_configured():
    """检查是否已经填写了真实的邮箱账号。"""
    if FROM_EMAIL.startswith("your_") or PASSWORD.startswith("your_"):
        return False
    if not RECIPIENTS:
        return False
    if any(r.endswith("@example.com") for r in RECIPIENTS):
        return False
    return True


def send_emails():
    """向收件人列表中的所有邮箱群发邮件。"""
    print(f"正在连接SMTP服务器 {SMTP_SERVER}:{SMTP_PORT} ...")
    context = ssl.create_default_context()

    # QQ、163等邮箱SMTP通常使用SSL加密连接
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
        smtp.login(FROM_EMAIL, PASSWORD)
        print("登录成功，开始群发邮件...\n")

        success, failed = 0, 0
        for recipient in RECIPIENTS:
            try:
                msg = build_email(recipient)
                smtp.sendmail(FROM_EMAIL, [recipient], msg.as_string())
                print(f"  [成功] {recipient}")
                success += 1
            except smtplib.SMTPException as e:
                print(f"  [失败] {recipient}：{e}")
                failed += 1

    print(f"\n群发完成，共{success}个成功，{failed}个失败。")


def main():
    make_test_files()

    # 不论是否配置真实账号，都先生成一份本地预览邮件
    preview_to = RECIPIENTS[0] if RECIPIENTS else "preview@example.com"
    save_preview(build_email(preview_to))

    if is_configured():
        send_emails()
    else:
        print("\n[提示] 尚未配置真实的SMTP账号，已跳过实际发送。")
        print("请编辑exp5.py顶部的常量后再次运行：")
        print("  FROM_EMAIL = '你的邮箱@xxx.com'")
        print("  PASSWORD   = '你的SMTP客户端授权码'")
        print("  RECIPIENTS = ['收件人1@xxx.com', '收件人2@xxx.com']")


if __name__ == "__main__":
    main()
