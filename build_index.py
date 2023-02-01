import os
import jieba
import re
from string import punctuation
import math
import numpy as np
import pickle

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
    #return count


def max_index(lst):
    """
    :param lst: 列表
    :return: 最大值的索引，可能有多个
    """
    index = []
    max_n = max(lst)
    for i in range(len(lst)):
        if lst[i] == max_n:
            index.append(i)
    return index  #返回一个列表

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
    # 读取文档名到列表，计算文档数量
    path = './dataset/web_data/'
    file_name_list = []
    file_num = 0
    if os.path.exists(path):
        file_name_list = os.listdir(path)
        file_num = len(file_name_list)
    # 按照文件名开头数字排序 解决了读取文件顺序的问题
    file_name_list.sort(key=lambda x: int(x.split('_')[0]))
    for i in range(file_num):
        with open(path + file_name_list[i], 'r', encoding='utf-8') as f:
            content = f.read()
    #for file_name in os.listdir('./dataset/web_data/'):
        # 找到输出跟输入查询词没有半毛钱关系的原因了，它读文件的时候不是按顺序读的
        # 0 10 11 12.。。。18 19 1 20 21.。。
        # 那我如果从10-99存文件呢？存到三位数、四位数好像还会出问题
        # 我先试一试----读取文件顺序对了，输出跟查询输入还是对不上
        #print(file_name)
        txt_num = txt_num + 1
        #with open('./dataset/web_data/' + file_name, 'r', encoding='utf-8') as f:
            #content = f.read()
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
        tmp = int(file_name_list[i].split('_')[0])
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
    #print(txt_words_list[0:2])
    return inverted_index, txt_num, txt_words_list


def query(inverted_index, txt_words_list, txt_num, query_str, url_id_dic):
    # tf 行数 = 词项的数目，列数 = 9（文档） + 1（查询）
    terms_num = len(inverted_index)
    tf_2D_arr = np.zeros((terms_num, txt_num + 1))
    #print(tf_2D_arr)
    # 所有单词
    terms_list = list(inverted_index.keys())
    # 循环计算tf数组
    for i in range(terms_num):
        tf_2D_arr[i][0] = cal_tf(terms_list[i], query_str)
        # 文档
        for j in range(1, txt_num + 1):
            tf_2D_arr[i][j] = cal_tf(terms_list[i], txt_words_list[j - 1])
    #print('==============================================================')
    #print('%% end compute tf')
    #print(tf_2D_arr)
    # 每个词项在整个文档集合的逆向文件频率
    idf_arr = np.zeros(terms_num)
    # 某个词项出现的文档数量， log（N/idf）
    for k in range(terms_num):
        # tf_2D_arr数组中每一行，非零元素的个数，不算第一列的（那是查询的词项）
        # idf_arr[k] = np.count_nonzero(tf_2D_arr[k][1:])
        # 包含第k个词条w的文档数
        tmp = len(inverted_index[terms_list[k]])
        #np.count_nonzero(tf_2D_arr[k][1:]
        idf_arr[k] = math.log((txt_num / tmp), 10)
        #idf_arr[k] = tmp
    #print(idf_arr)
    #print('%% end compute idf')
    # 向量中的每一项用tf*idf来表示
    # 查询向量
    query_vector = np.array([])
    for i in range(terms_num):
        query_vector = np.append(query_vector, idf_arr[i] * tf_2D_arr[i][0])
    #print('%% end compute query_vector')
    #print(query_vector)
    # 文档的查询向量，都存到一个列表中
    docs_vector = []
    for doc_num in range(txt_num):
        doc_vector = np.array([])
        for i in range(terms_num):
            doc_vector = np.append(doc_vector, idf_arr[i] * tf_2D_arr[i][doc_num + 1])
        docs_vector.append(doc_vector)
    #print(docs_vector)
    #print('%% end compute docs_vector')

    # 计算余弦相似度Cosine similarity
    docs_cos_sim = []
    for i in range(txt_num):
        num1 = query_vector.dot(docs_vector[i])
        num2 = np.linalg.norm(query_vector) * np.linalg.norm(docs_vector[i])
        # cos_sim = query_vector.dot(docs_vector[i]) / (np.linalg.norm(query_vector)*np.linalg.norm(docs_vector[i]))
        if num2 == 0:
            cos_sim = 0.0
        else:
            cos_sim = num1 / num2
        docs_cos_sim.append(cos_sim)

    #max_cos_sim = max(docs_cos_sim)
    sorted_indexes = sorted_index(docs_cos_sim)
    print("The top five query results are as follows————")
    title_dic = dict()
    with open("dataset/title_id_dic.pkl", "rb") as tf:
        title_dic = pickle.load(tf)
    rank = 1
    for i in range(5):
        tmp_i = txt_num - 1 - i
        # print(rank, ':', title_dic[sorted_indexes[tmp_i]+10], url_id_dic[sorted_indexes[tmp_i]+10])
        print('@', rank, ':', title_dic[sorted_indexes[tmp_i]], url_id_dic[sorted_indexes[tmp_i]])
        rank = rank + 1
    tf.close()
    print('The query has ended.Byebye~')
    # indexes = max_index(docs_cos_sim)
    # url_list = []
    # for i in indexes:
    #     url_list.append(url_id_dic[i])
    # print("query result is ......")
    # print(url_list)


# if __name__ == '__main__':
#     query_str = input("请输入您的查询词项，如输入多个，请以空格分割:")
#     print("--------------------开始查询--------------------------")
#     inverted_index, txt_num, txt_words_list = build_inverted_index()
#
#     query(inverted_index, txt_words_list, txt_num, query_str)
#     # str = '4_计算机科学与技术系.txt'
#     # tmp = str.split('_')
#     # print(tmp)
#     #build_inverted_index()
#     # 打印倒排索引
#     print(inverted_index)