import re

def cleanup_content(data):
    if type(data) == str:
        data = re.sub('\W+','',data)
        return data

    else:
        data =map(lambda x:re.sub('\W','',x), data)

        return [i for i in data]


def site_judge(url):
    w = url.split('.')[1]
    if w == 'ikea':
        return '10'
    elif w == 'trplus':
        return '20'
    elif w == 'pinkoi':
        return '30'
    else:
        return w
        
if __name__ == '__main__':
    data = "\n456\t"
    data = cleanup_content(data)
    print(data)

    datas = {'\n\neriyb\r  ', '\r\r  ldknf\n\n'}
    print(cleanup_content(datas))