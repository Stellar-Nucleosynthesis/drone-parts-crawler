import requests
from bs4 import BeautifulSoup
from details_parsing.websites import fpvua

def search_detail(name):
    try:
        url = "https://fpvua.com/search/?search=" + name
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        return [product.find('a')['href'] for product in soup.select('div.single-product[id^="product-card-"]')]
    except:
        print("Error while searching products urls")
        return []

def find_product_name(page):
    try:
        return fpvua.find_detail_model(page)
    except:
        print("Error while searching product name")
        return None

def find_sale_info(page):
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        price = soup.find("span", class_="autocalc-product-price").text.split()[0]
        is_available = soup.find("div", class_="stat-aval").text == "В наявності"
        return "FpvUA", price, is_available
    except:
        print("Error while searching product info")
        return None, None, None


