import romkan
import json

with open('term_bank_1.json', 'r', encoding='utf-8') as json_file:
    name_data = json.load(json_file)

def romaji_to_hiragana(romaji_text):
    hiragana_text = romkan.to_hiragana(romaji_text)
    return hiragana_text

for data in name_data:
     data[1] = romaji_to_hiragana(data[5][0].replace(" ", ""))

with open('term_bank_1.json', 'w', encoding='utf-8') as json_file:
    json.dump(name_data, json_file, indent=2, ensure_ascii=False)
