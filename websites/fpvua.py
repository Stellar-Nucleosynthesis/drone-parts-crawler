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

def find_attr(page, name):
    soup = BeautifulSoup(page.text, "html.parser")
    for li in soup.find_all("li"):
        span = li.find("span")
        if span and span.text.strip() == name:
            p = li.find("p")
            if p:
                return p.text.strip()
    return None

def find_detail_model(page):
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        container = soup.find("div", class_="product-container")
        product = container.find("span", recursive=False)
        return product.text.strip()
    except:
        return None

def find_detail_manufacturer(page):
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

frame_parsers = {}
frame_parsers["model"] = find_detail_model
frame_parsers["manufacturer"] = find_detail_manufacturer
frame_parsers["propellers_inches"] = lambda text: find_attr(text, "Розмір пропелерів")
frame_parsers["mass"] = lambda text: find_attr(text, "Вага")
frame_parsers["material"] = lambda text: find_attr(text, "Матеріал")
frame_parsers["size_mm"] = lambda text: find_attr(text, "Розмір рами")
frame_parsers["cam_mount_size"] = lambda text: find_attr(text, "Розмір кріплення камери")
frame_parsers["motor_mount_size"] = lambda text: find_attr(text, "Отвір для кріплення двигуна")
attr_parsers["Frame"] = frame_parsers

propeller_parsers = {}
propeller_parsers["model"] = find_detail_model
propeller_parsers["manufacturer"] = find_detail_manufacturer
propeller_parsers["material"] = lambda text: find_attr(text, "Матеріал")
propeller_parsers["propeller_size"] = lambda text: find_attr(text, "Розмір пропелера")
attr_parsers["Propeller"] = propeller_parsers

camera_parsers = {}
camera_parsers["model"] = find_detail_model
camera_parsers["manufacturer"] = find_detail_manufacturer
camera_parsers["mass"] = lambda text : find_attr(text, "Вага")
camera_parsers["size_mm"] = lambda text : find_attr(text, "Розмір")
camera_parsers["tvl"] = lambda text : find_attr(text, "Горизонтальна роздільна здатність")
camera_parsers["aspect_ratio"] = lambda text : find_attr(text, "Співвідношення сторін")
camera_parsers["video_format"] = lambda text : find_attr(text, "Система сигналу")
attr_parsers["Camera"] = camera_parsers

vtx_parsers = {}
def find_vtx_power(text):
    res = find_attr(text, "Вихідна потужність")
    if res:
        return res
    else:
        return (m.group() if (m := re.search(r'\b[\d.]+m?W\b', find_detail_model(text))) else None)

def find_vtx_frequency(text):
    res = find_attr(text, "Частота відеопередавача")
    if res:
        return res
    else:
        return (m.group() if (m := re.search(r'\b[\d.]+G\b', find_detail_model(text))) else None)

vtx_parsers["model"] = find_detail_model
vtx_parsers["manufacturer"] = find_detail_manufacturer
vtx_parsers["connector"] = lambda text : find_attr(text, "Роз'єм антенни")
vtx_parsers["max_power"] = find_vtx_power
vtx_parsers["video_format"] = lambda text : find_attr(text, "Відеоформат")
vtx_parsers["mass"] = lambda text : find_attr(text, "Вага")
vtx_parsers["size_mm"] = lambda text : find_attr(text, "Розмір")
vtx_parsers["frequency"] = find_vtx_frequency
attr_parsers["VTX"] = vtx_parsers