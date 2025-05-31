from bs4 import BeautifulSoup
from details_parsing.normalization import vtx, battery, propeller, antenna, motor, camera, frame, rx, stack
import re

url = "https://fpvua.com"

detail_paths = {
    "Frame" : "/komplektuiuchi/ramy",
    "Propeller" : "/komplektuiuchi/propelery",
    "Camera" : "/komplektuiuchi/kamery",
    "VTX" : "/komplektuiuchi/videoperedavachi",
    "RX" : "/komplektuiuchi/radioperedavachi",
    "Antenna" : "/komplektuiuchi/anteny",
    "Battery" : "/aksesuary/batarei",
    "Motor" : "/komplektuiuchi/motory",
    "Stack" : "/komplektuiuchi/polotni-kontrolery",
}

normalizers = {
    "Frame" : frame.normalize,
    "Propeller" : propeller.normalize,
    "Camera" : camera.normalize,
    "VTX" : vtx.normalize,
    "RX" : rx.normalize,
    "Antenna" : antenna.normalize,
    "Battery" : battery.normalize,
    "Motor" : motor.normalize,
    "Stack" : stack.normalize,
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

def find_detail_name(page):
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        container = soup.find("div", class_="product-container")
        product = container.find("span", recursive=False)
        return product.text.strip()
    except AttributeError:
        return None

def find_detail_model(page):
    # res = find_attr(page, ["Модель"])
    # if res:
    #     return res
    return find_detail_name(page)

def find_detail_manufacturer(page):
    res = find_attr(page, ["Виробник"])
    if res and res.strip():
        return res.strip()
    soup = BeautifulSoup(page.text, "html.parser")
    for li in soup.find_all("li"):
        span = li.find("span")
        if span and span.text.strip() == "Виробник:":
            p = li.find("p")
            if p:
                a = p.find("a")
                if a and a.text.strip():
                    return a.text.strip()
    return None

def find_photo_link(page):
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        container = soup.find("div", class_="swiper-slide")
        img = container.find("img", recursive=True)
        return img.get("data-src")
    except AttributeError:
        return None

attr_parsers = {}

frame = dict()
frame["model"] = find_detail_model
frame["manufacturer"] = find_detail_manufacturer
frame["propellers_inches"] = lambda text: find_attr(text, ["Розмір пропелерів"])
frame["mass"] = lambda text: find_attr(text, ["Вага"])
frame["material"] = lambda text: find_attr(text, ["Матеріал"])
frame["size_mm"] = lambda text: find_attr(text, ["Розмір рами", "Розмір (діагональ між центрами моторів)"])
frame["cam_mount_size"] = lambda text: find_attr(text, ["Розмір кріплення камери"])
frame["motor_mount_size"] = lambda text: find_attr(text, ["Отвір для кріплення двигуна"])
frame["photo_link"] = find_photo_link
attr_parsers["Frame"] = frame

prop = dict()
prop["model"] = find_detail_model
prop["manufacturer"] = find_detail_manufacturer
prop["material"] = lambda text: find_attr(text, ["Матеріал"])
prop["size_inches"] = lambda text: find_attr(text, ["Розмір пропелера", "Розмір"])
prop["photo_link"] = find_photo_link
attr_parsers["Propeller"] = prop

camera = dict()
camera["model"] = find_detail_model
camera["manufacturer"] = find_detail_manufacturer
camera["mass"] = lambda text : find_attr(text, ["Вага"])
camera["size_mm"] = lambda text : find_attr(text, ["Розмір"])
camera["mount_size"] = lambda text : "UNDEFINED"
camera["tvl"] = lambda text : find_attr(text, ["Горизонтальна роздільна здатність"])
camera["aspect_ratio"] = lambda text : find_attr(text, ["Співвідношення сторін"])
camera["video_format"] = lambda text : find_attr(text, ["Система сигналу"])
camera["photo_link"] = find_photo_link
attr_parsers["Camera"] = camera

vtx = dict()
def find_vtx_power(text):
    res = find_attr(text, ["Вихідна потужність"])
    if res:
        return res
    return m.group() if (m := re.search(r'\b[\d.]+m?W\b', find_detail_name(text))) else None

def find_vtx_frequency(text):
    res = find_attr(text, ["Частота відеопередавача"])
    if res:
        return res
    return m.group() if (m := re.search(r'\b[\d.]+G\b', find_detail_name(text))) else None

vtx["model"] = find_detail_model
vtx["manufacturer"] = find_detail_manufacturer
vtx["connector"] = lambda text : find_attr(text, ["Роз'єм антенни", "Інтерфейс антени"])
vtx["max_power"] = find_vtx_power
vtx["video_format"] = lambda text : find_attr(text, ["Відеоформат"])
vtx["mass"] = lambda text : find_attr(text, ["Вага"])
vtx["size_mm"] = lambda text : find_attr(text, ["Розмір"])
vtx["frequency"] = find_vtx_frequency
vtx["photo_link"] = find_photo_link
attr_parsers["VTX"] = vtx

rx = {}
def find_rx_frequency(text):
    res = find_attr(text, ["Диапазон частот"])
    if res:
        return res
    res = re.findall(r'\b[\d.]+(?:M|G|MHz|GHz)\b', find_detail_name(text))
    if res:
        return ", ".join(res)
    res = re.findall(r'\b[\d.]+(?:M|G|MHz|GHz)\b', find_detail_model(text))
    if res:
        return ", ".join(res)
    return None

def find_rx_protocol(text):
    res = find_attr(text, ["Протокол приймача"])
    if res:
        return res
    name = find_detail_name(text)
    return "ELRS" if "ELRS" in name or "ExpressLRS" in name \
        else "TBS Crossfire" if "Crossfire" in name or "TBS" in name else None


rx["model"] = find_detail_model
rx["manufacturer"] = find_detail_manufacturer
rx["connector"] = lambda text : find_attr(text, ["Роз'єм антенни", "Інтерфейс антени"])
rx["mass"] = lambda text : find_attr(text, ["Вага"])
rx["size_mm"] = lambda text : find_attr(text, ["Розмір", "Розміри"])
rx["frequency"] = find_rx_frequency
rx["protocol"] = find_rx_protocol
rx["photo_link"] = find_photo_link
attr_parsers["RX"] = rx

antenna = dict()
antenna["model"] = find_detail_model
antenna["manufacturer"] = find_detail_manufacturer
antenna["connector"] = lambda text : find_attr(text, ["Конектор"])
antenna["mass"] = lambda text : find_attr(text, ["Вага антени"])
antenna["size_mm"] = lambda text : find_attr(text, ["Довжина антени", "Розмір", "Розмір антени", "Розміри"])
antenna["frequency"] = lambda text : find_attr(text, ["Центральна частота", "Робоча частота", "Діапазон частот"])
antenna["dbi"] = lambda text : find_attr(text, ["Коефіцієнт підсилення"])
antenna["polarization"] = lambda text : find_attr(text, ["Поляризація"])
antenna["swr"] = lambda text : find_attr(text, ["Коефіцієнт стоячої хвилі (S.W.R.)"])
antenna["antenna_type"] = lambda text : "UNDEFINED"
antenna["photo_link"] = find_photo_link
attr_parsers["Antenna"] = antenna

battery = dict()
def find_battery_discharge(text):
    res = find_attr(text, ["Номінальний струм розряду", "Максимальний струм розряду"])
    if res:
        return res
    res = re.findall(r'\b\d+C\b', find_detail_name(text))
    if res:
        return ", ".join(res)
    return None

battery["model"] = find_detail_model
battery["manufacturer"] = find_detail_manufacturer
battery["mass"] = lambda text : find_attr(text, ["Вага"])
battery["size_mm"] = lambda text : find_attr(text, ["Розмір"])
battery["num_s"] = lambda text : find_attr(text, ["Кількість банок"])
battery["discharge_rate"] = find_battery_discharge
battery["battery_type"] = lambda text : find_attr(text, ["Тип акумулятора"])
battery["capacity"] = lambda text : find_attr(text, ["Номінальна ємність"])
battery["cable_connector"] = lambda text : find_attr(text, ["Тип розʼєму"])
battery["photo_link"] = find_photo_link
attr_parsers["Battery"] = battery

motor = dict()
def find_rotation_speed(text):
    res = find_attr(text, ["KV"])
    if res:
        return res
    res = re.findall(r'\b\d+KV\b', find_detail_name(text))
    if res:
        return ", ".join(res)
    return None

motor["model"] = find_detail_model
motor["manufacturer"] = find_detail_manufacturer
motor["mass"] = lambda text : find_attr(text, ["Вага (з дротом)"])
motor["size_mm"] = lambda text : find_attr(text, ["Розмір (В * Ш)"])
motor["mount_size"] = lambda text : "UNDEFINED"
motor["rotation_speed"] = find_rotation_speed
motor["range_s"] = lambda text : find_attr(text, ["Напруга", "Рекомендована батарея"])
motor["max_current"] = lambda text : find_attr(text, ["Максимальний струм"])
motor["max_power"] = lambda text : find_attr(text, ["Максимальна потужність"])
motor["photo_link"] = find_photo_link
attr_parsers["Motor"] = motor

stack = dict()
stack["model"] = lambda text : find_detail_model(text)
stack["manufacturer"] = find_detail_manufacturer
stack["mass"] = lambda text : find_attr(text, ["Вага"])
stack["size_mm"] = lambda text : find_attr(text, ["Розмір"])
stack["mount_size"] = lambda text : find_attr(text, ["Отвори для кріплення"])
stack["cable_connector"] = lambda text : find_attr(text, ["Кабель живлення"])
stack["working_current"] = lambda text : find_attr(text, ["Постійний струм"])
stack["max_current"] = lambda text : find_attr(text, ["Піковий струм"])
stack["range_s"] = lambda text : find_attr(text, ["Вхідна напруга"])
stack["photo_link"] = find_photo_link
attr_parsers["Stack"] = stack