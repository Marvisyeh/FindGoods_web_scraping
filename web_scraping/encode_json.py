
import json
# with open('./jason_ikea3.json') as f:
#     data = json.load(f)
# print(data)

with open('./json_footstools_01.json','r', encoding='utf-8') as f:
    data = json.load(f, encoding="utf-8")
# print(data)

with open('./CN_footstools.json', 'w', encoding='utf-8') as f2:
    # json.dump(data, f2, ensure_ascii=False)
    json.dump(data, f2, ensure_ascii=False, indent=2)#排序?


# #查詢
# with open('./json_footstools_02.json', 'r',encoding='utf-8') as f:
#     data = json.load(f, encoding='utf-8')
# li = []
# for i in data:
#     li.append(i['id'])
# #檢查是否有重複ID
# print(len(li))
# print(len(set(li)))       

# #     print(i[0]['id'])