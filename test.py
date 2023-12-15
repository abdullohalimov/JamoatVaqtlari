from bs4 import BeautifulSoup
import requests

def parse():
    page = requests.get("https://islom.uz/")
    soup = BeautifulSoup(page.text, "html.parser")
    # print(soup.prettify())
    a = soup.find('select', {"name": "region"}).findAll('option')
    mintaqalist = []
    for i in a:
        mtext = i.text
        mid = i['value']
        mintaqalist.append([mtext, mid])

    print(len(mintaqalist))
parse()