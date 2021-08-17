import requests
from bs4 import BeautifulSoup
import lxml
from time import sleep
import random
import json


list_url = []
url = f'https://www.bundestag.de/ajax/filterlist/de/abgeordnete/525246-525246?limit=20&noFilterSet=true&offset='
for i in range(0, 760, 20):
    page = url + str(i)
    sleep(random.randint(0, 2))
    zapros = requests.get(page)
    rezult = zapros.content
    soup = BeautifulSoup(rezult, 'lxml')
    persons = soup.find_all(class_="bt-open-in-overlay")

    for person in persons:
        pers_url = person.get('href')
        pers_name = person.get('title')

        list_url.append(pers_url)
print(list_url)
with open('urls.txt', 'r') as fl:
    for i in list_url:
        fl.write(f"https://www.bundestag.de{i}\n")
# class="bt-linkliste"bt-biografie-name



data_dict=[]
with open("urls.txt",'r') as file:
    sleep(random.randint(0, 3))

    spisok=[i.strip() for i in file.readlines()]
    for i in spisok:
        print(i)
        zapros = requests.get(i)
        rezult = zapros.content
        soup = BeautifulSoup(rezult, 'lxml')
        persons = soup.find(class_="bt-biografie-name").find('h3').text
        print(persons)
        stroka=persons.strip().split(',')
        name=stroka[0].strip()
        print(name)
        partija=stroka[1].strip()
        links = soup.find_all(class_="bt-link-extern")
        socset=[]
        for i in links:
            socset.append(i.get('href'))

        data={ 'name': name , 'partija':partija , 'socset': socset,}
        print(data)
        data_dict.append(data)


        with open('data.json','w') as fil:
            json.dump(data_dict, fil ,indent=4)
            
            


with open('data.json','r',encoding="utf-8") as file:
    a=json.load(file)
    spisok_partii=[]
    for i in a:
        spisok_partii.append(i['partija'].strip().replace('*',"").strip())

    variants=set(spisok_partii)

    for i in variants:
        print(f'В партии "{i}" {spisok_partii.count(i)} членов')

    itog_for_graph=[[i,spisok_partii.count(i)] for i in variants]

    print(itog_for_graph)

import matplotlib.pyplot as plt
fig1, ax1 = plt.subplots()
explode = [0.03 for i in itog_for_graph]

ax1.pie([i[1] for i in itog_for_graph], labels=[i[0] for i in itog_for_graph],explode=explode,shadow=True,autopct='%1.1f%%' )
ax1.axis('equal')
plt.show()