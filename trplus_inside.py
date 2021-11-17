def append_des(url):
    import requests
    from bs4 import BeautifulSoup
    from user_agent import generate_user_agent

    headers = {"User-Agent": generate_user_agent()}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    datas = soup.select('div[class="col-12 clearfix"]')
    # print(datas)
    theDict = {}
    for data in datas:
        describe = data.select('li')[0].text
        theDict["describe"] = describe
        # print(describe)
        # print("="*10)
        itemInfo =[size.text.strip('\r\n ').replace('\r\n ','').replace(' ','') for size in data.select('div[class="info__aspect"]')]
        theDict["itemInfo"] = itemInfo
        # print(sizes)
        # print("="*10)
    return theDict

if __name__ == "__main__":
    url = 'https://www.trplus.com.tw/p/014275486?cateCode=EC_10090063'
    theDict = append_des(url)
    print(theDict)
