"""爬取百度搜索结果中与"Python小屋"相关的信息，支持 mechanicalsoup 和 selenium 两种方式。"""

from pathlib import Path
from urllib.parse import urlencode
import argparse
import re
import time

import mechanicalsoup
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_KEYWORD = "Python小屋"
DEFAULT_OUTPUT = BASE_DIR / "exp3_baidu_results.txt"
BAIDU_SEARCH_URL = "http://www.baidu.com/s"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
)


def clean_text(text):
    """压缩空白字符。"""
    return re.sub(r"\s+", " ", text).strip()


def build_search_url(keyword, page):
    """构造百度搜索 URL，page 从 1 开始。"""
    query = urlencode({"wd": keyword, "pn": (page - 1) * 10, "ie": "utf-8"})
    return f"{BAIDU_SEARCH_URL}?{query}"


def fetch_page_with_mechanicalsoup(keyword, page):
    """使用 mechanicalsoup 获取页面 HTML。"""
    browser = mechanicalsoup.StatefulBrowser(
        user_agent=USER_AGENT,
        raise_on_404=True,
    )
    browser.open(build_search_url(keyword, page))
    return str(browser.get_current_page())


def fetch_page_with_selenium(keyword, page):
    """使用 Selenium 无头浏览器获取页面 HTML。"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--user-agent={USER_AGENT}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(build_search_url(keyword, page))
        time.sleep(2)  # 等待 JS 渲染完成
        return driver.page_source
    finally:
        driver.quit()


def parse_baidu_results(page_html, page):
    """解析百度搜索结果页，提取标题、链接和摘要。"""
    soup = BeautifulSoup(page_html, "html.parser")
    containers = soup.select("#content_left .result, #content_left .c-container")
    results = []
    seen = set()

    for container in containers:
        title_link = container.select_one("h3 a")
        if title_link is None:
            continue

        title = clean_text(title_link.get_text(" ", strip=True))
        url = title_link.get("href", "").strip()
        if not title or not url:
            continue

        summary_node = (
            container.select_one(".c-abstract")
            or container.find(class_=re.compile(r"(content-right|abstract|summary)"))
        )
        if summary_node is not None:
            summary = clean_text(summary_node.get_text(" ", strip=True))
        else:
            summary = clean_text(container.get_text(" ", strip=True).replace(title, "", 1))

        key = (title, url)
        if key in seen:
            continue
        seen.add(key)
        results.append({"page": page, "title": title, "url": url, "summary": summary})
    return results


def filter_related_results(results, keyword=DEFAULT_KEYWORD):
    """过滤出标题/摘要/链接中包含关键词的结果。"""
    key = keyword.lower().replace(" ", "")
    related = []
    for result in results:
        text = f"{result['title']} {result['summary']} {result['url']}"
        if key in text.lower().replace(" ", ""):
            related.append(result)
    return related


def write_results(results, output_path=DEFAULT_OUTPUT):
    """将搜索结果写入文本文件。"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fp:
        for index, result in enumerate(results, 1):
            fp.write(f"{index}. 第{result['page']}页\n")
            fp.write(f"标题：{result['title']}\n")
            fp.write(f"链接：{result['url']}\n")
            fp.write(f"摘要：{result['summary']}\n\n")


def crawl(keyword=DEFAULT_KEYWORD, pages=10, output_path=DEFAULT_OUTPUT, use_selenium=False):
    """主爬取流程：逐页抓取 → 解析 → 过滤 → 保存。"""
    all_related = []
    for page in range(1, pages + 1):
        if use_selenium:
            page_html = fetch_page_with_selenium(keyword, page)
        else:
            page_html = fetch_page_with_mechanicalsoup(keyword, page)

        results = parse_baidu_results(page_html, page)
        all_related.extend(filter_related_results(results, keyword))
        time.sleep(1)

    write_results(all_related, output_path)
    return all_related


def main():
    parser = argparse.ArgumentParser(description="爬取百度前十页中与 Python小屋 相关的信息。")
    parser.add_argument("--keyword", default=DEFAULT_KEYWORD)
    parser.add_argument("--pages", type=int, default=10)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--selenium", action="store_true", help="使用 Selenium 打开网页。")
    args = parser.parse_args()

    results = crawl(args.keyword, args.pages, args.output, args.selenium)
    print(f"共保存 {len(results)} 条相关结果到：{args.output}")


if __name__ == "__main__":
    main()
