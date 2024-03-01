#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bs4
import requests
import json
import time
import ast

# Assuming "your_file.txt" contains the text ["vn1","vn2"]
file_path = "cont.txt"

with open(file_path, "r") as file:
    file_content = file.read()

links_vn = ast.literal_eval(file_content)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"
}

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

    formatted_names = {}

    try:
        formatted_names = {f'{japanese_names[i]}': {'english_name': english_names[i], 'vn_name': vn_name} for i in range(len(english_names))}
    except:
        return

    with open('formatted_names4.json', 'a', encoding='utf-8') as json_file:
        json.dump(formatted_names, json_file, indent=2, ensure_ascii=False)

total_links = len(links_vn)

for i, link_vn in enumerate(links_vn, 1):
    scrape(link_vn)

    percentage_complete = (i / total_links) * 100
    print(f"Progress: {percentage_complete:.2f}%")

    time.sleep(1.7)

