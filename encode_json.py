# def trnas(path, )
import json
# with open('./jason_ikea3.json') as f:
#     data = json.load(f)
# print(data)

with open('./json_footstools.json','r', encoding='utf8') as f:
    data = json.load(f)
print(data)

with open('./CN_footstools.json', 'w', encoding='utf8') as f2:
        f2.write(json.dumps(data, ensure_ascii=False, indent=2))