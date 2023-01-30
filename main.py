import spider
import build_index
import pickle

if __name__ == '__main__':

    with open("dataset/url_id_dic.pkl", "rb") as tf:
        url_id_dic = pickle.load(tf)
    query_str = input("请输入您的查询词项，如输入多个，请以空格分割:")
    print("--------------------开始查询--------------------------")

    inverted_index, txt_num, txt_words_list = build_index.build_inverted_index()

    build_index.query(inverted_index, txt_words_list, txt_num, query_str, url_id_dic)
    tf.close()