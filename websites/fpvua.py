from bs4 import BeautifulSoup
import re

url = "https://fpvua.com"
detail_paths = {
    "Frame" : "/komplektuiuchi/ramy",
    "Propeller" : "/komplektuiuchi/propelery",
    "Camera" : "/komplektuiuchi/kamery",
    "VTX" : "/komplektuiuchi/videoperedavachi"
}

def detail_url_finder(sell_page):
    soup = BeautifulSoup(sell_page.text, "html.parser")
    return [product.find('a')['href'] for product in soup.select('div.single-product[id^="product-card-"]')]

def find_attr(page, values):
    soup = BeautifulSoup(page.text, "html.parser")
    for li in soup.find_all("li"):
        span = li.find("span")
        if span and span.text.strip() in values:
            p = li.find("p")
            if p:
                return p.text.strip()
    return None

def find_detail_model(page):
    res = find_attr(page, ["Модель"])
    if res:
        return res
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        container = soup.find("div", class_="product-container")
        product = container.find("span", recursive=False)
        return product.text.strip()
    except:
        return None

def find_detail_manufacturer(page):
    res = find_attr(page, ["Виробник"])
    if res:
        return res
    soup = BeautifulSoup(page.text, "html.parser")
    for li in soup.find_all("li"):
        span = li.find("span")
        if span and span.text.strip() == "Виробник:":
            p = li.find("p")
            if p:
                a = p.find("a")
                if a:
                    return a.text.strip()
    return None

attr_parsers = {}

frame = {}
frame["model"] = find_detail_model
frame["manufacturer"] = find_detail_manufacturer
frame["propellers_inches"] = lambda text: find_attr(text, ["Розмір пропелерів"])
frame["mass"] = lambda text: find_attr(text, ["Вага"])
frame["material"] = lambda text: find_attr(text, ["Матеріал"])
frame["size_mm"] = lambda text: find_attr(text, ["Розмір рами", "Розмір (діагональ між центрами моторів)"])
frame["cam_mount_size"] = lambda text: find_attr(text, ["Розмір кріплення камери"])
frame["motor_mount_size"] = lambda text: find_attr(text, ["Отвір для кріплення двигуна"])
attr_parsers["Frame"] = frame

prop = {}
prop["model"] = find_detail_model
prop["manufacturer"] = find_detail_manufacturer
prop["material"] = lambda text: find_attr(text, ["Матеріал"])
prop["propeller_size"] = lambda text: find_attr(text, ["Розмір пропелера", "Розмір"])
attr_parsers["Propeller"] = prop

camera = {}
camera["model"] = find_detail_model
camera["manufacturer"] = find_detail_manufacturer
camera["mass"] = lambda text : find_attr(text, ["Вага"])
camera["size_mm"] = lambda text : find_attr(text, ["Розмір"])
camera["tvl"] = lambda text : find_attr(text, ["Горизонтальна роздільна здатність"])
camera["aspect_ratio"] = lambda text : find_attr(text, ["Співвідношення сторін"])
camera["video_format"] = lambda text : find_attr(text, ["Система сигналу"])
attr_parsers["Camera"] = camera

vtx = {}
def find_vtx_power(text):
    res = find_attr(text, ["Вихідна потужність"])
    if res:
        return res
    return (m.group() if (m := re.search(r'\b[\d.]+m?W\b', find_detail_model(text))) else None)

def find_vtx_frequency(text):
    res = find_attr(text, ["Частота відеопередавача"])
    if res:
        return res
    return (m.group() if (m := re.search(r'\b[\d.]+G\b', find_detail_model(text))) else None)

vtx["model"] = find_detail_model
vtx["manufacturer"] = find_detail_manufacturer
vtx["connector"] = lambda text : find_attr(text, ["Роз'єм антенни", "Інтерфейс антени"])
vtx["max_power"] = find_vtx_power
vtx["video_format"] = lambda text : find_attr(text, ["Відеоформат"])
vtx["mass"] = lambda text : find_attr(text, ["Вага"])
vtx["size_mm"] = lambda text : find_attr(text, ["Розмір"])
vtx["frequency"] = find_vtx_frequency
attr_parsers["VTX"] = vtx