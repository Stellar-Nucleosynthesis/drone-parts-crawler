import pandas as pd
from bs4 import BeautifulSoup

from website_parsers import generic_parser
url = "https://fpvua.com"
paths = {"Camera" : "/komplektuiuchi/kamery"}

def product_url_parser(sell_page):
    soup = BeautifulSoup(sell_page.text, "html.parser")
    return [product.find('a')['href'] for product in soup.select('div.single-product[id^="product-card-"]')]

def find_attr(page, name):
    soup = BeautifulSoup(page.text, "html.parser")
    for li in soup.find_all("li"):
        span = li.find("span")
        if span and span.text.strip() == name:
            p = li.find("p")
            if p:
                return p.text.strip()
    return None

def find_model(page):
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        container = soup.find("div", class_="product-container")
        product = container.find("span", recursive=False)
        return product.text.strip()
    except:
        return None

attr_parsers = {}
attr_parsers["model"] = find_model
attr_parsers["manufacturer"] = lambda text : find_attr(text, "Виробник")
attr_parsers["mass"] = lambda text : find_attr(text, "Вага")
attr_parsers["size_mm"] = lambda text : find_attr(text, "Розмір")
attr_parsers["tvl"] = lambda text : find_attr(text, "Горизонтальна роздільна здатність")
attr_parsers["aspect_ratio"] = lambda text : find_attr(text, "Співвідношення сторін")
attr_parsers["video_format"] = lambda text : find_attr(text, "Система сигналу")


parser = generic_parser.MarketplaceParser(url, paths, product_url_parser, attr_parsers)
result = parser.parse()
for detail, df in result.items():
    print("Detail:", detail)
    print(df.to_string())
