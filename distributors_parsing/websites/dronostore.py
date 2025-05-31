import requests
from bs4 import BeautifulSoup

def search_detail(name):
    try:
        url = "https://drono.store/search?controller=search&s=" + name
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        return [product.find('a')['href'] for product in
                soup.findAll("div", class_="pro_first_box")]
    except:
        print("Error while searching products urls")
        return []

def find_product_name(page):
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        return soup.find("h1", class_="product_name").text
    except:
        print("Error while searching product name")
        return None

def find_sale_info(page):
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        price = soup.find("span", class_="price").text.split(',')[0]
        is_available = len(soup.findAll("div", class_="product-unavailable")) == 0
        return "Dronostore", price, is_available
    except:
        print("Error while searching product info")
        return None, None, None


