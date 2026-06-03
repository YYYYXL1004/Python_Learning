"""使用 Scrapy 爬取山东各城市天气预报并保存为文本文件。"""

from pathlib import Path
import html
import re

import scrapy
from scrapy.crawler import CrawlerProcess


BASE_DIR = Path(__file__).resolve().parent
START_URL = "http://www.weather.com.cn/shandong/index.shtml"
DEFAULT_OUTPUT = BASE_DIR / "exp2_weather.txt"


def clean_text(text):
    """去除 HTML 标签，压缩空白。"""
    text = re.sub(r"<.*?>", "", text, flags=re.S)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_weather_cards(page_html):
    """从页面 HTML 中提取各城市的气温和详情链接。"""
    block_match = re.search(
        r'<div\s+class="forecastBox"[^>]*>(.*?)</div>',
        page_html,
        flags=re.S,
    )
    if not block_match:
        return []

    records = []
    dl_blocks = re.findall(r"<dl>(.*?)</dl>", block_match.group(1), flags=re.S)
    for dl in dl_blocks:
        link_match = re.search(
            r'<dt>\s*<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>\s*</dt>',
            dl,
            flags=re.S,
        )
        temp_match = re.search(
            r"<span>([^<]+)</span>\s*</a>\s*/\s*<a><b>([^<]+)</b>",
            dl,
            flags=re.S,
        )
        if not link_match or not temp_match:
            continue

        records.append(
            {
                "city": clean_text(link_match.group(2)),
                "url": html.unescape(link_match.group(1)),
                "low": clean_text(temp_match.group(1)),
                "high": clean_text(temp_match.group(2)),
            }
        )
    return records


def write_weather(records, output_path=DEFAULT_OUTPUT):
    """将天气数据写入 TSV 文件。"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fp:
        fp.write("城市\t最低温\t最高温\t详情页\n")
        for record in records:
            fp.write("{city}\t{low}\t{high}\t{url}\n".format(**record))


class ShandongWeatherSpider(scrapy.Spider):
    """山东天气爬虫，抓取首页天气卡片数据。"""

    name = "shandong_weather"
    start_urls = [START_URL]
    custom_settings = {
        "LOG_LEVEL": "ERROR",
        "ROBOTSTXT_OBEY": False,
        "USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        ),
    }

    def __init__(self, output_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_path = Path(output_path or DEFAULT_OUTPUT)

    def parse(self, response):
        records = parse_weather_cards(response.text)
        write_weather(records, self.output_path)
        for record in records:
            yield record


def run(output_path=DEFAULT_OUTPUT):
    """启动 Scrapy 爬虫。"""
    process = CrawlerProcess(settings={"LOG_LEVEL": "ERROR"})
    process.crawl(ShandongWeatherSpider, output_path=str(output_path))
    process.start()


def main():
    run(DEFAULT_OUTPUT)
    print(f"山东城市天气数据已保存到：{DEFAULT_OUTPUT}")


if __name__ == "__main__":
    main()
