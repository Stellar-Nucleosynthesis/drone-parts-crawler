import requests
from bs4 import BeautifulSoup

def search_detail(name):
    try:
        url = "https://grotor.shop/katalog/search/?q=" + name
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        return ['https://grotor.shop' + product.find('a')['href'] for product in
                soup.findAll("div", class_="catalogCard-title")]
    except:
        print("Error while searching products urls")
        return []

def find_product_name(page):
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        return soup.find("h1", class_="product-title").text
    except:
        print("Error while searching product name")
        return None

def find_sale_info(page):
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        price = soup.find("div", class_="product-price__item").text.split()[0]
        is_available = soup.find("div", class_="product-header__availability").text == "В наявності"
        return "Grotor shop", price, is_available
    except:
        print("Error while searching product info")
        return None, None, None


