import re
import json

with open('combined.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

result = []
count = 1

for group in data:
    for japanese_name, info in group.items():
        japanese_parts = re.split(r'[ ＝・]', japanese_name)
        english_parts = info["english_name"].split()
        japanese_name_cleaned = japanese_name.replace(" ", "").replace("＝", "").replace("・", "")

        existing_entry = next((entry for entry in result if entry[0] == japanese_name_cleaned), None)
        if existing_entry is None:
            result.append([japanese_name_cleaned, "", "", "", 0, [info["english_name"]], count, ""])
            count += 1
        elif info["english_name"] not in existing_entry[5]:
            existing_entry[5].append(info["english_name"])

        if len(japanese_parts) == len(english_parts):
            for i in range(len(japanese_parts)):
                if any(entry[0] == japanese_parts[i] for entry in result):
                    existing_entry = next(entry for entry in result if entry[0] == japanese_parts[i])
                    if english_parts[i] not in existing_entry[5]:
                        existing_entry[5].append(english_parts[i])
                    
                else:    
                    entry = ["", "", "", "", 0, [], count, ""]
                    entry[0] = japanese_parts[i]
                    entry[5] = [english_parts[i]]
                    result.append(entry)
                    count += 1

with open('term_bank_1.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, indent=2, ensure_ascii=False)
