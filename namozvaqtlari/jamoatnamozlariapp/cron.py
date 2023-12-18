from bs4 import BeautifulSoup
import kronos
import random
import requests

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
    12: "Зул ҳижжа, Zul hijja"
}

regions = {
    1: [0, 1, 2, 3, 4],
    2: [6,7,8,9,10]
}

@kronos.register('0 0 1 * *')
def update():
    page = requests.get("https://islom.uz/")
    soup = BeautifulSoup(page.text, "html.parser")
    # print(soup.prettify())
    a = soup.find('select', {"name": "region"}).findAll('option')
    mintaqalist = []
    for i in a:
        mtext = i.text
        mid = i['value']
        mintaqalist.append([mtext, mid])



