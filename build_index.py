import os
import jieba
import re
from string import punctuation

# 定义倒排索引字典
inverted_index = {}
MAX_CUT_WORDS_NUM = 400


def build_inverted_index():
    # 读取txt文件
    for file_name in os.listdir('./dataset/web_data/'):
        with open('./dataset/web_data/' + file_name, 'r', encoding='utf-8') as f:
            content = f.read()
        # 去掉标点符号、小写、分词
        content = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), "", content)
        content = content.lower()
        words = jieba.lcut_for_search(content)[0:MAX_CUT_WORDS_NUM]
        #print(words)
        #words = ' '.join(jieba.lcut_for_search(content)[0:MAX_CUT_WORDS_NUM])
        #print("处理后的单词们", words)
        #print(type(words))
        #words = content.split()
        # 构建倒排索引
        # （0_计算机学院主页.txt ）是爬取的第几个url，可根据tmp获取url
        tmp = int(file_name.split('_')[0])
        for word in words:
            #print(word)
            if word not in inverted_index:
                inverted_index[word] = [tmp]
            else:
                if tmp not in inverted_index[word]:
                    inverted_index[word].append(tmp)



if __name__ == '__main__':
    # str = '4_计算机科学与技术系.txt'
    # tmp = str.split('_')
    # print(tmp)
    build_inverted_index()
    # 打印倒排索引
    print(inverted_index)