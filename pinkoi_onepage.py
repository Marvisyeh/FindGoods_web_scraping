import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import json

url = 'https://www.pinkoi.com/browse?category=5&subcategory=543'
headers = {'User-Agent' : generate_user_agent()}

res = requests.get(url, headers = headers)
soup = BeautifulSoup(res.text, 'html.parser')

final = []
for i in soup.select('script[type="application/ld+json"]'):
    for j in i.contents:
#         print(j['name'])
        final.append(json.loads(j))
# print(len(final))

# with open('./pinkoi_firestpage.json', 'w', encoding='utf-8') as f:
#     json.dump(final, f, ensure_ascii=False, indent=2)