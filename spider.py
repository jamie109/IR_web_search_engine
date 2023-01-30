import re
import os
import requests
from bs4 import BeautifulSoup
import IdMap
from string import punctuation
from time import sleep
import random

# MAX_NUM = 15

cc_base_url = 'http://cc.nankai.edu.cn'
# cur = 'http://cc.nankai.edu.cn'
#print(type(cur))
# 已经爬取过的网页，用集合
used_url_set = set()
# 将要爬取的网页，用列表保存，因为集合无序，无法遍历
to_use_url_list = ['http://cc.nankai.edu.cn']

# 这是需要登录、不在校园网内无法访问的url。爬不了的
dustbin_set = [
    'http://cc-backend.nankai.edu.cn',
    'http://yzxt.nankai.edu.cn/intern/frontend/web/index.php'
    ]

def get_url_data(base_url, count):
    print("@ start crawl the web page", base_url)
    if base_url in dustbin_set :
        to_use_url_list.remove(base_url)
        used_url_set.add(base_url)
        print('无法爬取该页面//$^$//')

        return count
    # 返回爬取到的网页
    html = requests.get(base_url, timeout=5)
    # 解决爬取网页乱码的问题
    html.encoding = 'utf-8'
    # 从网页抓取数据。
    soup = BeautifulSoup(html.text, 'lxml')
    # 找到了我想打开的文件夹
    #html_title = html.title.string
    tmp = soup.find('title')
    html_title = tmp.text # str类型
    # 去掉标题中的空格、标点符号
    #教代会、工会委员会.txt
    #html_title = html_title.replace("/", '')
    html_title = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), '', html_title)
    if html_title == '404NotFound':
        print('>>>404 Not Found, return')
        return count

    # 创建这个网页对应的文件，用来存储html文件
    #if not os.path.exists('dataset/web_data/' + html_title + '.txt'):
       # os.makedirs('dataset/web_data/' + html_title + '.txt')
    doc_html = open(os.path.join('dataset/html_data/' + '_' + str(count) + '_' + html_title + '.html'), 'w', encoding = 'utf-8')
    # 把这个网页（传进来的参数）内容填进去
    doc_html.write(html.text)
    doc_html.close()
    # print(">>>end write html")
    # 保存内容和标题
    # context
    doc_context = open(os.path.join('dataset/web_data/' + '_' +str(count) + '_' + html_title + '.txt'), 'w', encoding='utf-8')
    # 把url写在第一行
    url_tmp = base_url + '\n'
    doc_context.write(url_tmp)
    # print(">>>end write url")
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
    # print(">>>end write content")
    #print(">>>start look for hyperlinks")
    # url and anctext
    # 在html中，a表示超链接，例如<a href="http://www.w3school.com.cn">W3School</a>
    # 找到所有有超链接的地方，返回的可以看作列表吧，能用[i]索引
    data = soup.select('a')
    pages = set()
    # url_anc.write("+++ now is : " + cur + "\n")
    # 遍历这些超链接
    #num = 0
    for item in data:
        #print("处理前", item)
        # get_text()函数用来获取tag(这里是item)中包含的文本内容
        # 正则替换，就是把回车什么的去掉，变成一行文字
        text = re.sub("[\r \n\t]", '', item.get_text())
        #print("正则替换、处理后", text)
        # 如果text中没有内容,continue
        # text == None改为is
        if text is None or text == '':
            continue
        # 找item中的href,链接， 它是<a href="http://www.w3school.com.cn">W3School</a>
        url = item.get('href')
        # None改为is
        if url is None or url == '' or re.search('java|void', url) != None:
            # href=”javascript:void(0);”这个的含义是，让超链接去执行一个js函数，而不是去跳转到一个地址，
            # void(0)表示一个空的方法，也就是不执行js函数。
            # 应该是没有实际链接的意思,这种情况下continue
            continue
        # add header
        # 这个if语句用来完善一下前面我们得到的超链接
        # 如果他不是一个独立的链接,那么我们给它加上前缀,http://cc.nankai.edu.cn/链接
        if re.search('\.cn|\.com', url) is None:
            if re.match('http|https|www\.', url) is None:
                if re.match('\/', url) is None:
                    url = '/' + url
                # cc_base_url就是http://cc.nankai.edu.cn
                url = cc_base_url + url
        # 如果这个href里有文件
        #print("完善后的url",  url)
        if url not in used_url_set:
            #print(">>> >>>add ", url ,"to to_use_url_list")
            to_use_url_list.append(url)
        # num = num + 1
        # if num == 1:
        #      break
    # print(">>>remove ", base_url, "from to_use_url_list to used_url_set")
    to_use_url_list.remove(base_url)
    used_url_set.add(base_url)
    count = count + 1
    print("@ end crawl the web page", base_url, " bye~")
    return count


if __name__ == '__main__':
    # print("要爬取的网页", to_use_url_list)
    # test_html = get_html('https://cc.nankai.edu.cn/2022/1219/c13291a502413/page.htm')
    #get_url_data('https://cc.nankai.edu.cn/2022/1219/c13291a502413/page.htm')
    # print("要爬取的网页", to_use_url_list)
    # print("爬取过的网页", used_url_set)
    mycount = 0
    for i in range(0, 100):
        if to_use_url_list is not None and mycount < 50:
            print("@ 爬取次数", i)
            tmp = to_use_url_list[0]
            mycount = get_url_data(tmp, mycount)
            # 爬取网页 礼貌hh
            # 休息一下。太慢了，不休息了
            #sleep(random.randint(2, 3))
            #mycount = mycount + 1

    #print("要爬取的网页", to_use_url_list)




