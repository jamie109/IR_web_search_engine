import re
import os
import requests
from bs4 import BeautifulSoup
from string import punctuation

html = requests.get('http://cc.nankai.edu.cn/jswyjy/list.htm', timeout=2)
html.encoding = 'utf-8'
soup = BeautifulSoup(html.text, 'lxml')
    # 找到http://cc.nankai.edu.cn对应的id，因为一开始url_id_map是空的，这里就给添上了
    #addr_id = url_id_map.__getitem__(cur)
    # 找到了我想打开的文件夹
    #html_title = html.title.string
tmp = soup.find('title')
html_title = tmp.text # str类型
print(type(html_title))
print(html_title)
    # 去掉标题中的空格、标点符号
    #教代会、工会委员会.txt
print(html_title[2])
print(type(html_title[2]))
print(html_title[1])
print(type(html_title[1]))
# 忘记把返回值赋给html_title了
# 好气哦，啊啊啊
#html_title = html_title.replace("/", " ")
html_title = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), '', html_title)
print(html_title)