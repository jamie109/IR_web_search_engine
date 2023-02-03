import pickle
import networkx

def get_pagerank():
    """
    把权重写到本地文件了
    :return: 不需要返回，用到时直接读取本地文件即可
    """
    # 打开url跳转字典
    url_jump_dic = dict()
    with open("dataset/url_jump_dic.pkl", "rb") as tf:
        url_jump_dic = pickle.load(tf)
    # url对应的id
    url_find_id_dic = dict()
    with open("dataset/id_url_dic.pkl", "rb") as tf1:
        url_find_id_dic = pickle.load(tf1)
    print(url_find_id_dic)
    # 构造一个图
    graph = networkx.DiGraph()
    # 遍历字典中的所有url keys()
    for i in range(0, len(url_jump_dic)):
        for j in url_jump_dic[i]:
            if j in url_find_id_dic.keys():
                # 构造从 i 到 j 的边
                graph.add_edge(i, url_find_id_dic[j])
    print('add edges end')
    # 计算 page rank
    my_page_rank = networkx.pagerank(graph)
    print('pagerank result is ', my_page_rank)
    # 把这个字典写到本地文件中
    with open("dataset/id_pagerank_dic.pkl", "wb") as tf2:
        pickle.dump(my_page_rank, tf2)
    print("write pagerank dict finish")
    tf.close()
    tf1.close()
    tf2.close()


if __name__ == '__main__':
    get_pagerank()