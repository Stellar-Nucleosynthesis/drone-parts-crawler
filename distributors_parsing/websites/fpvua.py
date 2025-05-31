import requests
from bs4 import BeautifulSoup
from details_parsing.websites import fpvua

def search_detail(name):
    url = "https://fpvua.com/search/?search=" + name
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    return [product.find('a')['href'] for product in soup.select('div.single-product[id^="product-card-"]')]

def find_product_name(page):
    return fpvua.find_detail_model(page)

def find_sale_info(page):
    soup = BeautifulSoup(page.text, "html.parser")
    price = soup.find("span", class_="autocalc-product-price").text.split()[0]
    is_available = soup.find("div", class_="stat-aval").text == "В наявності"
    return "FpvUA", price, is_available


