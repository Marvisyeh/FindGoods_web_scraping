import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from tool import cleanup_content as clean

url = 'https://www.ikea.com.tw/zh/products/cushions-throws-and-chairpads/cushions/turill-art-80392966'
headers = {"User-Agent":generate_user_agent()}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text,'lxml')
item = soup.select('div[class="itemInfo mt-4"]')[0].h1.text
name = soup.select('div[class="itemInfo mt-4"]')[0].h6.text
inform = [p.text for p in soup.select('p[class="partNumber"]')]
price = clean(soup.select('div[class="itemInfo mt-4"]')[0].p.text)
imgs = ['https://www.ikea.com.tw'+i['href'] for i in soup.select('a[class="slideImg"]')]
table = soup.select('table')
table1 = [i.text for i in table[0].select('td')]
table2 =[i.text for i in table[1].select('td')]

print(item,name,price)
print(inform)
print(table1)
print(table2)
print(imgs)

