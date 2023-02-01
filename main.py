import build_index
import content_inverted_index
import pickle
import title_query
file_num = 250
from content_inverted_index import Invert_term
import math
from sklearn import preprocessing
import jieba
import re
from string import  punctuation
import numpy as np
import page_rank
import datetime

def content_query(file_num, query_str):
    # 加载倒排字典
    inverted_index_dic = dict()
    with open("dataset/inverted_index_dic.pkl", "rb") as tf:
        inverted_index_dic = pickle.load(tf)

    #query_str_list = query_str.split(' ')
    # 去标点、小写、分词
    query_str = query_str.replace(' ', '')
    content = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), "", query_str)
    content = content.lower()
    query_str_list = jieba.lcut_for_search(content)[0:10]
    # 查询结果初始化
    content_query_dic = dict()
    for i in range(file_num):
        content_query_dic[i] = 0.0

    for item in query_str_list:
        #print(item)
        #num = 0
        # 查询词在文档中出现过，为出现过的文档id对应的得分+1
        if item in inverted_index_dic.keys():
            for term_tmp in inverted_index_dic[item]:
                #print('@num', num, ':', term_tmp, ' for ', item)
                #num = num + 1
                #print(content_query_dic[term_tmp.txt_id],term_tmp.count )
                content_query_dic[term_tmp.txt_id] = content_query_dic[term_tmp.txt_id] + 1 + math.log(term_tmp.count, 10)* 0.1

    #print('内容查询结果：', content_query_dic)
    # 倒排字典存到本地
    with open("dataset/content_query_dic.pkl", "wb") as tf1:
        pickle.dump(content_query_dic, tf1)
    #print('store content_query_dic end')
    tf1.close()
    tf.close()
    # 返回列表
    content_query_list = list(content_query_dic.values())
    return content_query_list


def get_final_result(result_list):
    # url
    with open("dataset/url_id_dic.pkl", "rb") as tf1:
        url_id_dic = pickle.load(tf1)
    # 标题
    with open("dataset/title_id_dic.pkl", "rb") as tf:
        title_dic = pickle.load(tf)
    sorted_indexes = title_query.sorted_index(result_list)
    print("The top five query results are as follows")
    rank = 1
    for i in range(5):
        tmp_i = file_num - 1 - i
        # print(rank, ':', title_dic[sorted_indexes[tmp_i]+10], url_id_dic[sorted_indexes[tmp_i]+10])
        print('@', rank, ':', title_dic[sorted_indexes[tmp_i]],
              url_id_dic[sorted_indexes[tmp_i]])
        rank = rank + 1
    print('The query has ended.Byebye~')
    tf1.close()
    tf.close()


if __name__ == '__main__':
    query_str = input('Please enter your query content: ')
    # 查询日志
    now_time = str(datetime.datetime.now())
    query_log = '[' + now_time + '] query_str:' + query_str + '\n'
    with open("dataset/query_record_log.txt", "a", encoding='utf-8') as f:
        f.write(query_log)
    f.close()
    print("--------------------start query--------------------------")
    # content
    content_result_list = content_query(file_num, query_str)
    #print(sorted(content_result_list))
    # title
    title_result_list = title_query.title_query(query_str)
    #print(title_result_list)
    #print(sorted(title_result_list))

    # pagerank
    with open("dataset/id_pagerank_dic.pkl", "rb") as tf:
        pagerank_dic = pickle.load(tf)
    pagerank_list = list(pagerank_dic.values())

    # print("title only")
    # get_final_result(title_result_list)
    # print("content only")
    # get_final_result(content_result_list)
    # print("title and content")
    title_content = np.array(content_result_list) * 0.1 + np.array(title_result_list)
    # get_final_result(title_content)
    title_content_pagerank = title_content + np.array(pagerank_list)
    print('title_content_pagerank')
    get_final_result(title_content_pagerank)
    tf.close()


