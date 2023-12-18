from datetime import datetime
import logging
from bs4 import BeautifulSoup
import requests

def parse_mintaqa():
    page = requests.get("https://islom.uz/")
    soup = BeautifulSoup(page.text, "html.parser")
    # print(soup.prettify())
    a = soup.find('select', {"name": "region"}).findAll('option')
    mintaqalist = []
    for i in a:
        mtext = i.text
        mid = i['value']
        mintaqalist.append([mtext, mid])

    print(mintaqalist)

# http://api.aladhan.com/v1/gToH/07-12-2014

def parse_vaqtlar():
    page = requests.get("https://islom.uz/vaqtlar/27/12")
    soup = BeautifulSoup(page.text, "html.parser")
    # print(soup.prettify())
    vaqtlar = soup.find('table', {"class": "table table-bordered prayer_table"}).findAll('tr')
    last_hijri = 0
    hijri_month = 0
    headers = vaqtlar.pop(0)
    for vaqt in vaqtlar:
        text = vaqt.text.split()
        if last_hijri > int(text[0]) or last_hijri == 0:
            hijri_day = requests.get(f"http://api.aladhan.com/v1/gToH/{text[1]}-{datetime.now().month}-{datetime.now().year}")
            result = hijri_day.json()
            logging.warning(result)
            hijri_month = result['data']['hijri']['month']['number']
            logging.warning("Changing")
        last_hijri = int(text[0])
        print(f"{text[0]}-{hijri_month}")
        print(text)
        print("\n\n")


parse_mintaqa()