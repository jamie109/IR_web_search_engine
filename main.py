import build_index
import content_inverted_index
import pickle
import numpy as np

file_num = 241

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

    #print('内容查询结果：', content_query_dic)
    # 倒排字典存到本地
    with open("dataset/content_query_dic.pkl", "wb") as tf1:
        pickle.dump(content_query_dic, tf1)
    print('store content_query_dic end')
    tf1.close()
    tf.close()
    # 返回列表，用于测试
    content_query_list = list(content_query_dic.values())
    return content_query_list

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

if __name__ == '__main__':
    # 标题
    with open("dataset/title_id_dic.pkl", "rb") as tf:
        title_dic = pickle.load(tf)
    # url
    with open("dataset/url_id_dic.pkl", "rb") as tf1:
        url_id_dic = pickle.load(tf1)

    query_str = input('Please enter your query terms.\nIf you enter more than one, please separate them with spaces: ')
    print("--------------------开始查询--------------------------")
    # content
    my_content_query_list = content_inverted_index.content_query(file_num, query_str)
    # 对查询结果排序
    sorted_indexes = sorted_index(my_content_query_list)
    print("The top five query results are as follows————")
    rank = 1
    for i in range(5):
        tmp_i = file_num - 1 - i
        # print(rank, ':', title_dic[sorted_indexes[tmp_i]+10], url_id_dic[sorted_indexes[tmp_i]+10])
        print('@', rank, ':', title_dic[sorted_indexes[tmp_i]], url_id_dic[sorted_indexes[tmp_i]])
        rank = rank + 1
    print('The query has ended.Byebye~')

    tf1.close()
    tf.close()