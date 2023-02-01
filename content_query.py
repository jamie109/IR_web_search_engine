import jieba
import re
from string import punctuation
import pickle
import os
import numpy as np

# 停用词列表
def get_stopwords_list():
    hit_stopwords = [line.strip() for line in open(r'hit_stopwords.txt',encoding='UTF-8').readlines()]
    return hit_stopwords

def sorted_index(lst):
    """
    辅助函数，我觉得它可以用在计算完网页和查询的总相关性（pagerank 标题余弦相似度 内容倒排索引等等加起来）
    返回相关性由低到高的索引(url对应的id)
    :param lst: 列表
    :return: 根据元素进行排序的索引数组
    """
    sorted_indexes = []
    tmp = np.array(lst)
    # 返回根据元素由小到大排序的索引数组
    sorted_indexes = np.argsort(tmp)
    #print(type(sorted_indexes))
    #print(sorted_indexes)
    return sorted_indexes


def build_inverted_index():
    # 倒排索引字典
    inverted_index_dic = dict()
    # 最大分词次数
    cut_num = 400
    # 测试使用'./test_inverted_index/'
    # 运行使用'./dataset/web_data/'
    # 读取文档名到列表，计算文档数量
    path = 'dataset/web_data/'
    #path = 'test_inverted_index/'
    file_name_list = []
    file_num = 0
    # 存储所有txt文档中的单词列表
    txt_words_list = []
    if os.path.exists(path):
        file_name_list = os.listdir(path)
        file_num = len(file_name_list)
    # 按照文件名开头数字排序 解决了读取文件顺序的问题
    file_name_list.sort(key=lambda x: int(x.split('_')[0]))
    for i in range(file_num):
        with open(path + file_name_list[i], 'r', encoding='utf-8') as f:
            content = f.read()
        # 去标点、小写、分词
        content = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), "", content)
        content = content.lower()
        words = jieba.lcut_for_search(content)[0:cut_num]
        #print(words)
        # 去掉停用词
        stopwords_list = get_stopwords_list()
        for word in words:
            if word in stopwords_list:
                words.remove(word)
        #print('==========去停用词===========\n', words, '\n==================end===================')
        # 所有文档中的所有单词
        txt_words_list.append(words)
        # 构建倒排索引
        # （0_计算机学院主页.txt ）是爬取的第几个url，可根据tmp获取url
        tmp = int(file_name_list[i].split('_')[0])
        for word in words:
            if word not in inverted_index_dic:
                inverted_index_dic[word] = [tmp]
            else:
                if tmp not in inverted_index_dic[word]:
                    inverted_index_dic[word].append(tmp)
        f.close()
    #print(inverted_index_dic)
    # 倒排字典存到本地
    with open("dataset/inverted_index_dic.pkl", "wb") as tf:
        pickle.dump(inverted_index_dic, tf)
    print('store inverted_index_dic end')
    tf.close()

    return  file_num


def content_query(file_num, query_str):
    # 加载倒排字典
    inverted_index_dic = dict()
    with open("dataset/inverted_index_dic.pkl", "rb") as tf:
        inverted_index_dic = pickle.load(tf)

    query_str_list = query_str.split(' ')
    # 查询结果初始化
    content_query_dic = dict()
    for i in range(file_num):
        content_query_dic[i] = 0

    for item in query_str_list:
        # 查询词在文档中出现过，为出现过的文档id对应的得分+1
        if item in inverted_index_dic.keys():
            for txt_id in inverted_index_dic[item]:
                if txt_id not in content_query_dic.keys():
                    content_query_dic[txt_id] = 1
                else:
                    content_query_dic[txt_id] = content_query_dic[txt_id] + 1

    print('内容查询结果：', content_query_dic)
    # 倒排字典存到本地
    with open("dataset/content_query_dic.pkl", "wb") as tf1:
        pickle.dump(content_query_dic, tf1)
    print('store content_query_dic end')
    tf1.close()
    tf.close()
    # 返回列表，用于测试
    content_query_list = list(content_query_dic.values())
    return content_query_list



if __name__ == '__main__':
    # 标题
    with open("dataset/title_id_dic.pkl", "rb") as tf:
        title_dic = pickle.load(tf)
    # url
    with open("dataset/url_id_dic.pkl", "rb") as tf1:
        url_id_dic = pickle.load(tf1)
    # 输入查询
    my_query_str = input('Please enter your query terms.\nIf you enter more than one, please separate them with spaces: ')
    my_file_num = build_inverted_index()
    my_content_query_list = content_query(my_file_num, my_query_str)

    # 对查询结果排序
    sorted_indexes = sorted_index(my_content_query_list)
    print("The top five query results are as follows————")
    rank = 1
    for i in range(5):
        tmp_i = my_file_num - 1 - i
        # print(rank, ':', title_dic[sorted_indexes[tmp_i]+10], url_id_dic[sorted_indexes[tmp_i]+10])
        print('@', rank, ':', title_dic[sorted_indexes[tmp_i]], url_id_dic[sorted_indexes[tmp_i]])
        rank = rank + 1
    tf.close()
    tf1.close()
    print('The query has ended.Byebye~')
