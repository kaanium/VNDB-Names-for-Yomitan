#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bs4
import os
import requests
import json
import time

links = []
links_vn = []
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"}


def scrape(link_vn):
    response = requests.get(link_vn, headers=headers)
    print(response)
    try:
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    vn_name_element = soup.select_one("body > main > article:nth-child(1) > h1")
    vn_name = vn_name_element.text.strip() if vn_name_element else ''
    english_names = [name.text.strip() for name in soup.select("body > main > article > div > table > thead > tr > td > a")]
    japanese_names = [name.text.strip() for name in soup.select("body > main > article > div > table > thead > tr > td > small")]
    
    if not japanese_names:
        return

    try:
        formatted_names = {f'{japanese_names[i]}': {'english_name': english_names[i], 'vn_name': vn_name} for i in range(len(english_names))}
    except:
        return

    with open('formatted_names.json', 'a', encoding='utf-8') as json_file:
        json.dump(formatted_names, json_file, indent=2, ensure_ascii=False)


def get_links(link):
    global links

    response = requests.get(link, headers=headers)
    print(response, 1)
    try:
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    links += soup.select('body>main>form>article>table>tr>td>a')
    try:
        next_link = soup.find("a", {"rel": "next"})
        next_link = "https://vndb.org/v" + next_link.get("href")
        time.sleep(1.5)
        get_links(next_link)
    except Exception:
        return


get_links("https://vndb.org/v")

for i in range(len(links)):
    href = links[i]['href']
    links_vn.append("https://vndb.org" + href + "/chars#chars")


for link_vn in links_vn:
    scrape(link_vn)
    time.sleep(1.5)

