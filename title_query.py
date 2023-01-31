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
    :param a_doc: 文档
    :return: 词项在文档中出现的次数，加一，取log
    """
    count = 0
    # print(type(a_doc))
    if type(a_doc) == type('abd'):
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


def title_query(path, query_str, url_id_dic):
    """
    进行查询输入跟标题的查询，保存余弦相似度字典到本地（id对应的）
    :param path: 网页内容txt路径
    :param query_str: 要查询的内容，字符串格式，空格隔开
    :param url_id_dic: 根据id查找url的字典
    """
    print("Query is in progress, please wait......")
    cut_num = 400
    file_num = 0
    file_name_list = []
    # 读取文档名到列表，计算文档数量
    if os.path.exists(path):
        file_name_list = os.listdir(path)
        file_num = len(file_name_list)
    # 按照文件名开头数字排序 解决了读取文件顺序的问题
    file_name_list.sort(key=lambda x: int(x.split('_')[0]))
    # 标题字典，根据id查找标题
    title_dic = {}
    title_list = []
    title_terms_list = []
    titles_term_for_txt = []
    for i in range(file_num):
        #print(file_name_list[i])
        tmp = file_name_list[i].split('_')[1][:-4]
        tmp = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), "", tmp)
        tmp = tmp.lower()
        words = jieba.lcut_for_search(tmp)[0:cut_num]
        title_terms_list.extend(words)
        #title_dic[tmp] = i + 10
        #title_dic[i+10] = tmp
        title_dic[i] = tmp
        titles_term_for_txt.append(words)
        #print(titles_term_for_txt[i])
        #title_list.append(tmp)
    #print(len(title_terms_list))
    # 根据id查找标题字典保存到本地，输出查询结果时会用到
    with open("dataset/title_id_dic.pkl", "wb") as tf:
        pickle.dump(title_dic, tf)
    tf.close()
    # 借助集合去重
    title_terms_list = list(set(title_terms_list))
    title_terms_num = len(title_terms_list)
    title_terms_list = sorted(title_terms_list)
    # 行数 = 词项的数目
    # 列数 = 9（文档） + 1（查询）
    tf_2D_arr = np.zeros((title_terms_num, file_num + 1))
    # 循环计算tf数组
    for i in range(title_terms_num):
        tf_2D_arr[i][0] = cal_tf(title_terms_list[i], query_str)
        for j in range(1, file_num + 1):
            tf_2D_arr[i][j] = cal_tf(title_terms_list[i], titles_term_for_txt[j - 1])
    # 查看tf
    #print(tf_2D_arr)
    idf_arr = np.zeros(title_terms_num)

    # 某个词项出现的文档数量， log（N/idf）
    for k in range(title_terms_num):
        # tf_2D_arr数组中每一行，非零元素的个数，不算第一列的（那是查询的词项）
        # idf_arr[k] = np.count_nonzero(tf_2D_arr[k][1:])
        idf_arr[k] = math.log(file_num / np.count_nonzero(tf_2D_arr[k][1:]), 10)
        # 向量中的每一项用tf*idf来表示
        # 查询向量
    query_vector = np.array([])
    for i in range(title_terms_num):
        query_vector = np.append(query_vector, idf_arr[i] * tf_2D_arr[i][0])
    # print(query_vector)
    # 文档的查询向量，都存到一个列表中
    docs_vector = []
    for doc_num in range(file_num):
        doc_vector = np.array([])
        for i in range(title_terms_num):
            doc_vector = np.append(doc_vector, idf_arr[i] * tf_2D_arr[i][doc_num + 1])
        docs_vector.append(doc_vector)
    # print(docs_vector)
    # 计算余弦相似度Cosine similarity
    docs_cos_sim = []
    for i in range(file_num):
        num1 = query_vector.dot(docs_vector[i])
        num2 = np.linalg.norm(query_vector) * np.linalg.norm(docs_vector[i])
        # cos_sim = query_vector.dot(docs_vector[i]) / (np.linalg.norm(query_vector)*np.linalg.norm(docs_vector[i]))
        if num2 == 0:
            cos_sim = 0.0
        else:
            cos_sim = num1 / num2
        docs_cos_sim.append(cos_sim)
    #print(docs_cos_sim)
    #indexes = max_index(docs_cos_sim)
    """
    用来测试标题查询
    sorted_indexes = sorted_index(docs_cos_sim)
    print("The top five query results are as follows————")
    rank = 1
    for i in range(5):
        tmp_i = file_num - 1 - i
        #print(rank, ':', title_dic[sorted_indexes[tmp_i]+10], url_id_dic[sorted_indexes[tmp_i]+10])
        print('@', rank, ':', title_dic[sorted_indexes[tmp_i]], url_id_dic[sorted_indexes[tmp_i]])
        rank = rank + 1

    print('The query has ended.Byebye~')
    #print(title_dic)
    #print(type(title_dic.keys())) <class 'dict_keys'>
    """
    # 改成字典
    title_cos_sim_dic = dict()
    for i in range(file_num):
        title_cos_sim_dic[i] = docs_cos_sim[i]
    #print(title_cos_sim_dic)
    # 标题余弦相似度字典保存到本地
    with open("dataset/title_cos_sim_dic.pkl", "wb") as tf1:
        pickle.dump(title_cos_sim_dic, tf1)
    tf1.close()



def test_read_files(path):
    """
    测试文件读取顺序的
    :param path:
    :return:
    """
    # 读取文档名到列表，计算文档数量
    file_name_list = []
    file_num = 0
    if os.path.exists(path):
        file_name_list = os.listdir(path)
        file_num = len(file_name_list)
    # 按照文件名开头数字排序
    file_name_list.sort(key=lambda x: int(x.split('_')[0]))
    for i in range(file_num):
        print(file_name_list[i])


if __name__ == '__main__':
    with open("dataset/url_id_dic.pkl", "rb") as tf:
        url_id_dic = pickle.load(tf)
    #query_str = input("请输入您的查询词项，如输入多个，请以空格分割:")
    query_str = input("Please enter your query terms.\nIf you enter more than one, please separate them with spaces: ")
    # 测试用的
    files_path_test = './test_inverted_index/'
    files_path = './dataset/web_data/'
    my_docs_cos_sim = title_query(files_path, query_str, url_id_dic)
    #print(my_docs_cos_sim)
    tf.close()
    # a = sorted_index([9,8,7,6,5])
    # for i in range(len(a)):
    #     print(a[i])

    #test_read_files(files_path)