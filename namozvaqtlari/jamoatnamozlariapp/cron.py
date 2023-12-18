from datetime import datetime
import logging
from bs4 import BeautifulSoup
import kronos
import random
import requests
from .models import Mintaqa, NamozVaqti

hijri_months = {
    1: "Муҳаррам, Muharram",
    2: "Сафар, Safar",
    3: "Рабиъул аввал, Rabi’ul avval",
    4: "Рабиъул ахир, Rabi’ul axir",
    5: "Жумадул аввал, Jumadul avval",
    6: "Жумадул ахир, Jumadul axir",
    7: "Ражаб, Rajab",
    8: "Шаъбон, Sha’bon",
    9: "Рамазон, Ramazon",
    10: "Шаввол, Shavvol",
    11: "Зул қаъда, Zul qa’da",
    12: "Зул ҳижжа, Zul hijja",
}

regions = {1: [0, 1, 2, 3, 4, 27], 2: [6, 7, 8, 9, 10]}


@kronos.register("0 0 1 * *")
def update():
    page = requests.get("https://islom.uz/")
    soup = BeautifulSoup(page.text, "html.parser")
    # print(soup.prettify())
    a = soup.find("select", {"name": "region"}).findAll("option")
    mintaqalist = []
    for i in a:
        mtext = i.text
        mid = int(i["value"])
        mregion = 99
        for key, value in regions.items():
            if mid in value:
                mregion = key

        mintaqalist.append([mtext, mid, mregion])

    for mintaqa in mintaqalist:
        a, b = Mintaqa.objects.get_or_create(
            viloyat=mintaqa[2], name_uz=mintaqa[0], mintaqa_id=mintaqa[1]
        )
        a.save()
    mintaqalar = Mintaqa.objects.all()
    for mintaqa in mintaqalar:
        page = requests.get(
            f"https://islom.uz/vaqtlar/{mintaqa.mintaqa_id}/{datetime.now().month}"
        )
        soup = BeautifulSoup(page.text, "html.parser")
        # print(soup.prettify())
        vaqtlar = soup.find(
            "table", {"class": "table table-bordered prayer_table"}
        ).findAll("tr")
        last_hijri = 0
        hijri_month = 0
        headers = vaqtlar.pop(0)
        for vaqt in vaqtlar:
            text = vaqt.text.split()
            if last_hijri > int(text[0]) or last_hijri == 0:
                hijri_day = requests.get(
                    f"http://api.aladhan.com/v1/gToH/{text[1]}-{datetime.now().month}-{datetime.now().year}"
                )
                result = hijri_day.json()
                logging.warning(result)
                hijri_month = result["data"]["hijri"]["month"]["number"]
                logging.warning("Changing")
            last_hijri = int(text[0])
            a, b = NamozVaqti.objects.get_or_create(
                mintaqa=mintaqa,
                milodiy_oy=datetime.now().month,
                milodiy_kun=int(text[1]),
                xijriy_oy=hijri_month,
                xijriy_kun=int(text[0]),
                vaqtlari=f"{text[3]} | {text[4]} | {text[5]} | {text[6]} | {text[7]} | {text[8]}",
            )
            a.save()
