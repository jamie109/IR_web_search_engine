import os
import jieba
import re
from string import punctuation
import math
import numpy as np


def cal_tf(term, a_doc):
    """
    :param term: 词项
    :param a_doc: 文档或查询字符串
    :return: 词项在文档中出现的次数，加一，取log
    """
    count = 0
    # print(type(a_doc))
    # 输入的查询字符串
    if isinstance(a_doc, str):
        a_doc = a_doc.split(' ')
    for t in a_doc:
        #print(t)
        if t == term:
            count += 1
    return math.log(count + 1, 10)


def build_inverted_index():
    """
    :return: 倒排索引字典,txt文档数目
    """
    # 倒排索引字典
    inverted_index = {}
    # 最大分词次数
    cut_num = 400
    # txt文档数目
    txt_num = 0
    # 存储所有txt文档中的单词列表
    txt_words_list = []
    # 测试使用'./test_inverted_index/'
    # 运行使用'./dataset/web_data/'
    for file_name in os.listdir('./test_inverted_index/'):
        txt_num = txt_num + 1
        with open('./test_inverted_index/' + file_name, 'r', encoding='utf-8') as f:
            content = f.read()
        # 去掉标点符号、小写、分词
        content = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), "", content)
        content = content.lower()
        words = jieba.lcut_for_search(content)[0:cut_num]
        txt_words_list.append(words)
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
            # if word not in term_list:
            #     term_list.append(word)
        f.close()
    return inverted_index, txt_num, txt_words_list


def query(inverted_index, txt_words_list, txt_num, query_str):
    # tf 行数 = 词项的数目，列数 = 9（文档） + 1（查询）
    terms_num = len(inverted_index)
    tf_2D_arr = np.zeros((terms_num, txt_num + 1))
    print(tf_2D_arr)
    # 所有单词
    terms_list = list(inverted_index.keys())
    # 循环计算tf数组
    for i in range(terms_num):
        tf_2D_arr[i][0] = cal_tf(terms_list[i], query_str)
        # 文档
        for j in range(1, txt_num + 1):
            tf_2D_arr[i][j] = cal_tf(terms_list[i], txt_words_list[j - 1])
    print('==============================================================')
    print(tf_2D_arr)

if __name__ == '__main__':
    query_str = input("请输入您的查询词项，如输入多个，请以空格分割:")
    print("--------------------开始查询--------------------------")
    inverted_index, txt_num, txt_words_list = build_inverted_index()

    query(inverted_index, txt_words_list, txt_num, query_str)
    # str = '4_计算机科学与技术系.txt'
    # tmp = str.split('_')
    # print(tmp)
    build_inverted_index()
    # 打印倒排索引
    #print(inverted_index)