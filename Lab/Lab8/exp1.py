"""爬取中国工程院院士列表，保存每位院士的简介文本和照片。"""

from pathlib import Path
from urllib.parse import urljoin
import argparse
import html
import re
import ssl
import time
import urllib.request


BASE_DIR = Path(__file__).resolve().parent
BASE_URL = "https://www.cae.cn"
LIST_URL = "https://www.cae.cn/cae/html/main/col48/column_48_1.html"
OUTPUT_DIR = BASE_DIR / "exp1_files"
TEXT_DIR = OUTPUT_DIR / "texts"
IMAGE_DIR = OUTPUT_DIR / "images"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
)


def fetch_bytes(url, timeout=20):
    """下载 URL 的原始字节，自动处理空格编码和 SSL 兼容。"""
    url = url.replace(" ", "%20")
    ctx = ssl.create_default_context()
    ctx.set_ciphers("DEFAULT:@SECLEVEL=1")  # 兼容老服务器的 SSL 配置
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout, context=ctx) as response:
        return response.read()


def fetch_html(url):
    return fetch_bytes(url).decode("utf-8", "ignore")


def clean_text(text):
    """去除 HTML 标签，保留纯文本内容。"""
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = html.unescape(text)
    text = text.replace("\u2002", " ").replace("\u2003", " ")
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def safe_filename(name):
    return re.sub(r'[\\/:*?"<>|]', "_", name).strip()


def parse_academician_links(index_html):
    """从列表页提取每位院士的姓名和详情页链接。"""
    links = []
    seen = set()
    pattern = r'<li\s+class="name_list">\s*<a\s+href="([^"]+)"[^>]*>(.*?)</a>\s*</li>'
    for href, name_html in re.findall(pattern, index_html, flags=re.S):
        href = html.unescape(href).strip()
        if not href.startswith(("http://", "https://", "/")):
            continue
        url = urljoin(BASE_URL, href)
        name = clean_text(name_html)
        if not name or url in seen:
            continue
        seen.add(url)
        links.append({"name": name, "url": url})
    return links


def parse_profile(profile_html, fallback_name):
    """从详情页提取姓名、简介和照片 URL。"""
    name_match = re.search(
        r'<div\s+class="right_md_name">\s*(.*?)\s*</div>',
        profile_html,
        flags=re.S,
    )
    intro_match = re.search(
        r'<div\s+class="intro">\s*(.*?)\s*</div>',
        profile_html,
        flags=re.S,
    )
    image_block = re.search(
        r'<div\s+class="info_img">(.*?)</div>',
        profile_html,
        flags=re.S,
    )
    image_match = None
    if image_block:
        image_match = re.search(r'<img[^>]+src="([^"]+)"', image_block.group(1), flags=re.S)

    name = clean_text(name_match.group(1)) if name_match else fallback_name
    intro = clean_text(intro_match.group(1)) if intro_match else ""
    photo_url = urljoin(BASE_URL, html.unescape(image_match.group(1))) if image_match else ""
    return {"name": name, "intro": intro, "photo_url": photo_url}


def unique_stem(name, used):
    """生成不重复的文件名前缀。"""
    stem = safe_filename(name)
    if stem not in used:
        used[stem] = 1
        return stem
    used[stem] += 1
    return f"{stem}_{used[stem]}"


def save_profile(profile, detail_url, stem):
    """将院士简介保存为文本文件，照片保存为图片文件。"""
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    text_path = TEXT_DIR / f"{stem}.txt"
    with open(text_path, "w", encoding="utf-8") as fp:
        fp.write(f"姓名：{profile['name']}\n")
        fp.write(f"详情页：{detail_url}\n")
        fp.write(f"照片：{profile['photo_url']}\n\n")
        fp.write(profile["intro"])

    image_path = None
    if profile["photo_url"]:
        try:
            suffix = Path(profile["photo_url"]).suffix or ".jpg"
            image_path = IMAGE_DIR / f"{stem}{suffix}"
            with open(image_path, "wb") as fp:
                fp.write(fetch_bytes(profile["photo_url"]))
        except Exception as e:
            print(f"  ⚠ 图片下载失败 {profile['name']}: {e}")
            image_path = None

    return text_path, image_path


def crawl(limit=None, delay=0.2):
    """主爬取流程：获取列表页 → 逐个抓取详情 → 保存文件。"""
    index_html = fetch_html(LIST_URL)
    links = parse_academician_links(index_html)
    if limit is not None:
        links = links[:limit]

    used_names = {}
    saved = []
    for item in links:
        profile_html = fetch_html(item["url"])
        profile = parse_profile(profile_html, item["name"])
        stem = unique_stem(profile["name"], used_names)
        saved.append((profile["name"], *save_profile(profile, item["url"], stem)))
        time.sleep(delay)
    return saved


def main():
    parser = argparse.ArgumentParser(description="爬取中国工程院院士简介和照片。")
    parser.add_argument("--limit", type=int, default=None, help="只爬取前 N 位，便于测试。")
    parser.add_argument("--delay", type=float, default=0.2, help="每个详情页之间的暂停秒数。")
    args = parser.parse_args()

    saved = crawl(args.limit, args.delay)
    print(f"已保存 {len(saved)} 位院士资料到：{OUTPUT_DIR}")


if __name__ == "__main__":
    main()
