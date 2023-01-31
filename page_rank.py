import pickle as pkl
import networkx as nx
# 读取文件路径，存储每个url页面可以有效跳转的url（都用id表示）
url_list_DICT_PATH = "F:\\workspace\\pycharmProjects\\IR-hw6-Web-Search-Engine-main\\dataset\\data_out\\url_list.dict"
# 最终结果保存到这里，存储每个url的网页权重
id_pagerank_DICT_PATH = "F:\\workspace\\pycharmProjects\\IR-hw6-Web-Search-Engine-main\\dataset\\data_out\\id_pagerank.dict"
# 爬取的url数量
URL_NUM = 23136
# 用来调整网页权重的，因为这个权重还需要跟标题啊内容啊什么的余弦相似度进行计算（可能是相加？它们应该有各自的权重）
PGRANK_ADJUST_PARAM = 1e4


def gen_pagerank():
    # 打开了一个字典
    f = open(url_list_DICT_PATH, 'rb')
    p = pkl.load(f)
    # 构造一个图
    G = nx.DiGraph()
    # 遍历字典中的所有元素
    for i in range(0, len(p)):
        # URL_NUM 是url数目
        if i > URL_NUM:
            break
        # i 应该表示 url 的 id
        # 如果字典中存了 id 为 i 的 url
        if i in p.keys():
            # 对于 i 对应的结果（可能是个列表）
            # 里面存的是 id 为 i 的 url 页面可以跳转到的 url 的 id 们
            # 构造从 i 到 j 的边
            for j in p[i]:
                G.add_edge(i, j)
    print("add finish..")
    # 计算 page rank，pr是个字典吗？
    pr = nx.pagerank(G)
    # 构造一个字典，用来存每个 id（唯一对应一个 url） 对应的网页权重
    print(pr)
    prdic = {}
    for node, pageRankValue in pr.items():
        if node <= URL_NUM:
            prdic[node] = pageRankValue * PGRANK_ADJUST_PARAM
    print("calc pagerank finish..")
    print(prdic)
    # 把这个字典写到本地文件中
    fdump = open(id_pagerank_DICT_PATH, "wb")
    pkl.dump(prdic, fdump, 0)
    print("write into id_pagerank.dict finish..")


if __name__ == '__main__':
    pass