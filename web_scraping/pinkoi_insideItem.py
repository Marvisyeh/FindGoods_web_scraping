def plus_des(url):
    import requests
    from bs4 import BeautifulSoup
    from user_agent import generate_user_agent
    import json
    from time import sleep

    headers = {'User-Agent' : generate_user_agent()}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    name = soup.select('h1[class="title translate"]')[0].text
    price = soup.select('div[class="price-wrap"]')[0].text.strip('\n')
    imgUrl = ['https:'+i['src'].replace('80x80','800x0') for i in soup.select('div[class="photos-thumbs"]')[0].select('img')]
    des = {i.select('dt')[0].text.strip('\n').strip(' ').strip('\n').strip('：'):i.select('dd')[0].text.strip('\n').strip(' ').strip('\n') for i in soup.select('div[class="m-product-list-item"]')}
    del des['付款方式']
    plus = {"name":name, "price":price, "imgUrl":imgUrl, "others":des}
    return plus

if __name__ == "__main__":
    url = 'https://www.pinkoi.com/product/Q7pE2Zfm?category=5&ref_itemlist=8QNVk85K'
    print(plus_des(url))