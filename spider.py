import re
import os
import requests
from bs4 import BeautifulSoup
import IdMap

# 文件和id
doc_id_map = IdMap.IdMap()  # doc to id

url_id_map = IdMap.IdMap()  # url to id

base_url = 'http://cc.nankai.edu.cn'
cur = 'http://cc.nankai.edu.cn'

def get_html(url):
    print("try to get: ", url)
    try:
        temp = requests.get(url, timeout=2)
        temp.encoding = 'utf-8'
    except:
        return None
    return temp


def get_html_data(html):
    soup = BeautifulSoup(html.text, 'lxml')
    # 找到http://cc.nankai.edu.cn对应的id，因为一开始url_id_map是空的，这里就给添上了
    addr_id = url_id_map.__getitem__(cur)
    # 找到了我想打开的文件夹
    #html_title = html.title.string
    tmp = soup.find('title')
    html_title = tmp.text

    # 创建这个网页对应的文件，用来存储html文件
    #if not os.path.exists('dataset/web_data/' + html_title + '.txt'):
       # os.makedirs('dataset/web_data/' + html_title + '.txt')
    doc_html = open(os.path.join('dataset/html_data/' + html_title + '.html'), 'w', encoding='utf-8')
    # 把这个网页（传进来的参数）内容填进去
    doc_html.write(html.text)
    doc_html.close()
    print("html文件写入结束。")
    # 保存内容和标题
    # context
    doc_context = open(os.path.join('dataset/web_data/' + html_title + '.txt'), 'w', encoding='utf-8')

    # 这个总链接（我爬虫的这个页面）的标题写进去
    data = soup.select('head')
    for item in data:
        # 变成一行
        text = re.sub('[\r \n\t]', '', item.get_text())
        if text is None or text == '':
            continue
        doc_context.write(text)

    # 这个总链接（我爬虫的这个页面）的文字写进去
    data = soup.select('body')
    for item in data:
        text = re.sub('[\r \n\t]', '', item.get_text())
        if text is None or text == '':
            continue
        doc_context.write(text)
    doc_context.close()
    print("txt文件写入结束。")


if __name__ == '__main__':
    test_html = get_html('https://cc.nankai.edu.cn/2022/1219/c13291a502413/page.htm')
    get_html_data(test_html)




