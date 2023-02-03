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
import tkinter
from tkinter import *
from tkinter import messagebox
import random

# 全局，不作为参数输入
my_user_term = None
global_age = 0
# user_name =None
# global_user_name = None


class user_term:
    """
    保存用户信息的类
    """
    name = None
    age = None
    sex = None
    # passport = None

    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
        # self.passport = passport


def recm_based_on_age(user_age):
    if user_age < 25:
        recm_list =[
        '学术纵横10位优秀研究生获评南开十杰荣誉称号广播南开大学\n http://news.nankai.edu.cn/gb/system/2021/01/15/030044176.shtml',
        '南开大学博士生获评全国大学生年度人物提名奖南开要闻南开大学\n http://news.nankai.edu.cn/ywsd/system/2023/01/24/030054301.shtml',
        '1437期2022级新生开学典礼隆重举行南开大学报南开大学\n http://news.nankai.edu.cn/nkdxb/system/2022/09/27/030052954.shtml',
        '专题2022年南开大学毕业季南开要闻南开大学\n http://news.nankai.edu.cn/xlzt/system/2022/06/22/030051775.shtml',
        '1435期2022届毕业生扬帆逐梦启新程南开大学报南开大学\n http://news.nankai.edu.cn/nkdxb/system/2022/06/27/030051859.shtml',
        '南开欢迎你5000余名硕博新生报到南开要闻南开大学\n http://news.nankai.edu.cn/ywsd/system/2022/09/03/030052668.shtml',
        '学习二十大精神牢记总书记嘱托南开大学师生座谈会召开南开要闻南开大学\n http://news.nankai.edu.cn/ywsd/system/2023/01/17/030054271.shtml',
        '组图新学期首日科学有效防控安全有序开学光影南开南开大学\n http://news.nankai.edu.cn/gynk/system/2021/01/08/030043781.shtml',
        '爱国有原则敢讲真话我眼中的杨振宁先生南开故事南开大学\n http://news.nankai.edu.cn/nkrw/system/2022/09/26/030052949.shtml'
        ]
    else:
        recm_list = [
            '今晚报潜心科研创新勇攀世界科技高峰媒体南开南开大学\n http://news.nankai.edu.cn/mtnk/system/2023/01/19/030054288.shtml',
            '1413期我校与滨海新区全面深化战略合作南开大学报南开大学\n http://news.nankai.edu.cn/nkdxb/system/2021/04/20/030045575.shtml',
            '杨振宁先生百岁华诞葛墨林院士讲述杨振宁先生的南开故事上南开故事南开大学\n http://news.nankai.edu.cn/nkrw/system/2022/09/26/030052948.shtml',
            '1422期化学学科创建100周年纪念大会召开南开大学报南开大学\n http://news.nankai.edu.cn/nkdxb/system/2021/11/01/030048602.shtml',
            '津云南开大学以人才学科之石筑牢高等教育之基媒体南开南开大学\n http://news.nankai.edu.cn/mtnk/system/2023/01/19/030054289.shtml',
            '学术纵横校学术委员会考核评审百名青年学科带头人及团队项目广播南开大学\n http://news.nankai.edu.cn/gb/system/2021/01/15/030044192.shtml',
            '学术纵横南开大学图灵书院开班跨学科打造师生共同体广播南开大学\n http://news.nankai.edu.cn/gb/system/2021/01/15/030044183.shtml',
            '这四年南开谱写新篇南开要闻南开大学\n http://news.nankai.edu.cn/ywsd/system/2023/01/16/030054264.shtml'
        ]
    #随机选3个
    recm_list_3_news = random.sample(recm_list, 3)
    return recm_list_3_news


def content_query(is_wildcard, file_num, query_str):
    """
    如果是通配查询，要对输入字符串进行处理，？单个字符，*任意字符序列
    :param file_num:
    :param query_str:
    :return:
    """
    # 加载倒排字典
    inverted_index_dic = dict()
    with open("dataset/inverted_index_dic.pkl", "rb") as tf:
        inverted_index_dic = pickle.load(tf)
    query_str_list = []
    # 通配查询
    if is_wildcard:
        query_str_list = title_query.proc_wildcard(list(inverted_index_dic.keys()), query_str)
    else:
        # 方式一：分词处理
        # 去标点、小写、分词
        query_str = query_str.replace(' ', '')
        content = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), "", query_str)
        content = content.lower()
        query_str_list = jieba.lcut_for_search(content)[0:10]
        # 方式二，输入关键字以空格分割
        # query_str_list = query_str.split(' ')

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
                content_query_dic[term_tmp.txt_id] = content_query_dic[term_tmp.txt_id] + 1 + math.log(term_tmp.count, 10) * 0.1

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
    """
    输出结果，传到Tkinter前端中
    :param result_list:
    :return:
    """
    # 输出结果
    output_res = "The top five query results are as follows————\n"
    # url
    with open("dataset/url_id_dic.pkl", "rb") as tf1:
        url_id_dic = pickle.load(tf1)
    # 标题
    with open("dataset/title_id_dic.pkl", "rb") as tf:
        title_dic = pickle.load(tf)
    sorted_indexes = title_query.sorted_index(result_list)
    print("The top five query results are as follows————")
    rank = 1
    for i in range(5):
        tmp_i = file_num - 1 - i
        # print(rank, ':', title_dic[sorted_indexes[tmp_i]+10], url_id_dic[sorted_indexes[tmp_i]+10])
        output_res = output_res + ' @ '+ str(rank) + ': '+ title_dic[sorted_indexes[tmp_i]] +'\n url: '+ url_id_dic[sorted_indexes[tmp_i]] + '\n'
        print('@', rank, ':', title_dic[sorted_indexes[tmp_i]],
              url_id_dic[sorted_indexes[tmp_i]])
        rank = rank + 1
    print('The query has ended.Byebye~')
    tf1.close()
    tf.close()
    # 增加个性化推荐
    output_res = output_res + '\nYou may be interested in the following news————\n'
    print('user age is ', global_age)
    # print(f"\nthe output_res is ", output_res )
    to_recommed_3_news = recm_based_on_age(global_age)
    for i in range(3):
        output_res = output_res + '@ ' + to_recommed_3_news[i] + '\n'
    return output_res


# def log_in_v1():
#     """
#     登录/注册
#     :return: 用户的年龄和性别
#     """
#     users_info_dic = dict()
#     user_name = input('Welcome!\nEnter user name: ')
#     # 核对是否注册过
#     try:
#         with open("dataset/users_info_dic.pkl", "rb") as tf:
#             users_info_dic = pickle.load(tf)
#     except:
#         users_info_dic = dict()
#     tf.close()
#     if user_name not in users_info_dic.keys():
#         print('Error, you have not registered yet.')
#         user_name = input('Enter the user name to register: ')
#         user_age = input('Enter your age: ')
#         user_sex = input('Enter your sex(male or female): ')
#         user_info = user_term(user_name, user_age, user_sex)
#         users_info_dic[user_name] = user_info
#         with open("dataset/users_info_dic.pkl", "wb") as t:
#             pickle.dump(users_info_dic, t)
#         t.close()
#         print('Congratulations! The registration is successful.')
#     else:
#         print('Login success, ', user_name, '!')
#     return users_info_dic[user_name]
#
#
# def to_query():
#     """
#     根据输入查询相关网页链接
#     :return:
#     """
#     query_str = input('Please enter your query content: ')
#     # 查询日志
#     now_time = str(datetime.datetime.now())
#     query_log = '[' + now_time + '] user_name:@' + my_user_term.name + ' query_str:' + query_str + '\n'
#     with open("dataset/query_record_log.txt", "a", encoding='utf-8') as f:
#         f.write(query_log)
#     f.close()
#     print("--------------------start query--------------------------")
#     # content
#     content_result_list = content_query(file_num, query_str)
#     # print(sorted(content_result_list))
#     # title
#     title_result_list = title_query.title_query(query_str)
#     # print(title_result_list)
#     # print(sorted(title_result_list))
#
#     # pagerank
#     with open("dataset/id_pagerank_dic.pkl", "rb") as tf:
#         pagerank_dic = pickle.load(tf)
#     pagerank_list = list(pagerank_dic.values())
#
#     # print("title only")
#     # get_final_result(title_result_list)
#     # print("content only")
#     # get_final_result(content_result_list)
#     # print("title and content")
#     title_content = np.array(content_result_list) * 0.1 + np.array(title_result_list)
#     # get_final_result(title_content)
#     title_content_pagerank = title_content + np.array(pagerank_list)
#     print('title_content_pagerank')
#     get_final_result(title_content_pagerank)
#     tf.close()
#     print("------------------------end-----------------------------")
#     # print('猜你喜欢：')

# def jump_to_query(parent):
    # pass

def query_result_view(is_wildcard,query_str_entry, user_name_str, parent_plus):
    """
    输出查询结果,
    :param query_str_entry:查询字符串	输入控件
    :param user_name_str:用户名
    :param parent:
    :return:
    """
    query_str = query_str_entry.get()
    user_name = user_name_str
    # 查询日志
    now_time = str(datetime.datetime.now())[0:-7]
    if is_wildcard:
        query_way = 'Wildcard_query'
    else:
        query_way = 'In-station_query'
    query_log = '[' + now_time + '] '+'OP: '+ query_way +', user_name:@' + user_name + ', query_str:' + query_str + '\n'
    with open("dataset/query_record_log.txt", "a", encoding='utf-8') as f:
        f.write(query_log)
    f.close()
    print('@ write query log over.')
    # 开始查询
    print('start query time ： ', str(datetime.datetime.now())[0:-7])
    # content
    content_result_list = content_query(is_wildcard, file_num, query_str)
    # title
    title_result_list = title_query.title_query(is_wildcard, query_str)
    # pagerank
    with open("dataset/id_pagerank_dic.pkl", "rb") as tf:
        pagerank_dic = pickle.load(tf)
    pagerank_list = list(pagerank_dic.values())
    # 组合相似度
    # 根据年龄为用户设定标题、内容的比例
    if global_age < 25:
        title_content = np.array(content_result_list) * 0.1 + np.array(title_result_list)
    else:
        title_content = np.array(content_result_list) * 0.3 + np.array(title_result_list)*0.05
    title_content_pagerank = title_content + np.array(pagerank_list)
    print('@ title_content_pagerank query')
    res = get_final_result(title_content_pagerank)
    print('end query time ： ',str(datetime.datetime.now())[0:-7])
    tf.close()
    query_result_view_win = Tk()
    query_result_view_win.title('query result of [' + query_str + ']')
    query_result_view_win.geometry("700x400+400+200")
    Label(query_result_view_win, text=res, font="微软雅黑 10",justify='left').grid(row=0, column=0, columnspan=2, sticky="w",
                                                                   pady=10)
    # parent.destroy()
    # if parent_plus is not None:
    #     parent_plus.destroy()


def query(flag, user_name, user_age, user_sex, parent, parent_plus = None):
    """
    输入查询字符串，站内查询
    :param flag:是否需要保存用户信息
    :param user_name:用户名 字符串
    :param user_age:年龄	输入控件
    :param user_sex:性别 输入控件
    :param parent:
    :param parent_plus:如果是从log in窗口跳过来的，关闭log in窗口
    :return:
    """
    user_name_str = user_name.get()
    # 从sign up跳过来的，需要保存用户信息
    # if flag:
    #     # 创建用户信息
    #     print('@create user info')
    #     print(f'name = {user_name.get()}')
    #     if user_age.get() == '':
    #         print('age = 0')
    #         user_age_int = 0
    #     else:
    #         user_age_int = int(user_age.get())
    #         print(f'age = {user_age_int}')
    #     print(f'sex = {user_sex.get()}')
    #     create_user_term = user_term(user_name.get(), user_age_int, user_sex.get())
    #     # 加入用户信息字典，保存
    #     print('add user info to users_info_dic.pkl')
    #     users_info_dic[user_name.get()] = create_user_term
    #     with open("dataset/users_info_dic.pkl", "wb") as t:
    #         pickle.dump(users_info_dic, t)
    #     t.close()
    #     print(f'@Congratulations,{user_name.get()}! The registration is successful.')
    #     # 注册日志
    #     now_time = str(datetime.datetime.now())[0:-7]
    #     query_log = '[' + now_time + '] ' + 'OP: sign up, ' + 'user_name:@' + user_name.get() + ', user_age:' + str(user_age_int) + ', user_sex:' + user_sex.get()+ '\n'
    #     with open("dataset/query_record_log.txt", "a", encoding='utf-8') as f:
    #         f.write(query_log)
    #     f.close()
    #     print('@ write user registration information log over.')
    # 查询
    query_start = Tk()
    query_start.title('In-station query')
    query_start.geometry("350x200+400+200")
    input_query_str_entry = Entry(query_start, width=30)
    Label(query_start, text='\n Input query statement:', font="微软雅黑 14").grid(row=0, column=0,
                                                                columnspan=2, sticky="w", pady=10)
    input_query_str_entry.grid(row=1, column=0, sticky="e", padx=20)
    Button(query_start, text='View query results', font="宋体 14", relief="raised",
           command=lambda:query_result_view(False, input_query_str_entry, user_name_str,
                                            parent_plus)).grid(row=2, column=0, columnspan=2, pady=20)
    #parent.destroy()
    # if parent_plus is not None:
    #     parent_plus.destroy()


def wildcard_query(user_name, parent, parent_plus = None):
    """
    通配查询
    :param user_name:
    :param parent:
    :param parent_plus:
    :return:
    """
    user_name_str = user_name.get()
    wildcard_query_start = Tk()
    wildcard_query_start.title('wildcard query')
    wildcard_query_start.geometry("350x300+400+200")
    input_query_str_entry = Entry(wildcard_query_start, width=30)
    Label(wildcard_query_start, text='\n "?" match a character', font="微软雅黑 14").grid(row=0,
                                                                column=0, columnspan=2, sticky="w", pady=10)
    Label(wildcard_query_start,
          text='"*" Matches any character sequence',font="微软雅黑 14").grid(row=1, column=0,
                                                                         columnspan=2, sticky="w", pady=10)
    Label(wildcard_query_start,
          text=' Input query statement:',font="微软雅黑 14").grid(row=2, column=0,
                                                              columnspan=2, sticky="w",pady=10)

    input_query_str_entry.grid(row=3, column=0, sticky="e", padx=20)
    Button(wildcard_query_start, text='View query results', font="宋体 14", relief="raised",
           command=lambda: query_result_view(True, input_query_str_entry, user_name_str,
                                             parent_plus)).grid(row=4, column=0, columnspan=2, pady=20)
    # if parent_plus is not None:
    #     parent_plus.destroy()


def save_info(user_name, user_age, user_sex, parent):
    # 解决出现两个弹窗的问题
    root = Tk()
    root.withdraw()
    # 创建用户信息
    user_name_str = user_name.get()
    print(f'@create user info for {user_name_str}')
    print(f'name = {user_name.get()}')
    if user_age.get() == '':
        print('age = 0')
        user_age_int = 0
    else:
        user_age_int = int(user_age.get())
        print(f'age = {user_age_int}')
    print(f'sex = {user_sex.get()}')
    create_user_term = user_term(user_name.get(), user_age_int, user_sex.get())
    # 加入用户信息字典，保存
    print('add user info to users_info_dic.pkl')
    users_info_dic[user_name.get()] = create_user_term
    with open("dataset/users_info_dic.pkl", "wb") as t:
        pickle.dump(users_info_dic, t)
    t.close()
    print(f'@Congratulations,{user_name.get()}! The registration is successful.')
    # 注册日志
    now_time = str(datetime.datetime.now())[0:-7]
    query_log = '[' + now_time + '] ' + 'OP: sign_up, ' + 'user_name:@' + user_name.get() + ', user_age:' \
                + str(user_age_int) + ', user_sex:' + user_sex.get() + '\n'
    with open("dataset/query_record_log.txt", "a", encoding='utf-8') as f:
        f.write(query_log)
    f.close()
    print('@ write user registration information log over.')
    # askyesno返回True False, askquestion返回“Yes" ”No“
    tmp = tkinter.messagebox.askyesno(message='The registration is successful.\nDo you want to start now?')
    if tmp == False:
        return
    else:
        login_jump_query(user_name, parent)
    # tkinter.messagebox.showinfo(message="The registration is successful.")
    # 获取全局变量用户年龄
    global global_age
    global_age = user_age_int


def sign_up(flag, parent):
    """
    用户注册，需输入姓名，年龄，性别
    :param flag:传到query函数，用于判断是否需要在字典中写入用户信息（sign up结束后才写入）
    :param parent:
    :return:
    """
    signup = Tk()
    signup.title('sign up')
    signup.geometry("350x300+400+200")
    user_name = Entry(signup, width=30)
    user_age = Entry(signup, width=30)
    user_sex = Entry(signup, width=30)
    Label(signup, text='\n  Enter your name:', font="微软雅黑 12").grid(row=0,
                                                                    column=0, columnspan=2, sticky="w", pady=10)
    user_name.grid(row=1, column=1, sticky="e", padx=30)
    Label(signup, text='  Enter your age:', font="微软雅黑 12").grid(row=2,
                                                                 column=0, columnspan=2, sticky="w", pady=10)
    user_age.grid(row=3, column=1, sticky="e", padx=30)
    Label(signup, text='  Enter your sex(male or female):', font="微软雅黑 12").grid(row=4,
                                                                 column=0, columnspan=2, sticky="w", pady=10)
    user_sex.grid(row=5, column=1, sticky="e", padx=30)
    #保存注册信息
    Button(signup, text='save info', font="楷体 10", relief="raised",
           command=lambda: save_info(user_name, user_age, user_sex, signup)).grid(row=8,
                                                                                  column=0, columnspan=2, pady=20)
    # # 站内查询
    # Button(signup, text="In-station query", font="楷体 10", relief="raised",
    #        command=lambda: query(flag, user_name, user_age, user_sex, signup)).grid(
    #                                                                 row=9, column=0, columnspan=2, pady=20)
    # # 通配查询
    # Button(signup, text="Wildcard query", font="楷体 10", relief="raised",
    #        command=lambda: wildcard_query(user_name, signup)).grid(row=10, column=0, columnspan=2, pady=20)

    parent.destroy()


def login_jump_query(user_name_entry, parent):
    """
    选择查询方式，站内、通配？
    :param user_name_entry:
    :param parent:
    :return:
    """
    jump_to_query = Tk()
    jump_to_query.title('In-station or wildcard?')
    jump_to_query.geometry("350x300+400+200")
    # 站内查询
    Label(jump_to_query, text='Choose in-station query:', font="微软雅黑 14").grid(row=0,
                                                    column=0, columnspan=2, sticky="w", pady=10)
    Button(jump_to_query, text="In-station query", font="楷体 14", relief="raised",
           command=lambda: query(flag=False, user_name=user_name_entry, user_age=None, user_sex=None,
                                 parent=jump_to_query,parent_plus=parent)).grid(row=1, column=0, columnspan=2, pady=20)

    # 通配查询
    Label(jump_to_query, text='\nChoose wildcard query:', font="微软雅黑 14"
          ).grid(row=2, column=0, columnspan=2, sticky="w", pady=10)
    Button(jump_to_query, text="Wildcard query", font="楷体 14", relief="raised",
           command=lambda: wildcard_query(user_name_entry, jump_to_query, parent)).grid(row=3, column=0, columnspan=2, pady=20)
    #parent.destroy()

def check_info(e1, parent):
    """
    检验用户先前是否注册过，如没有注册过，转到注册界面
    :param e1: 用户名的输入控件
    :param parent:
    :return:
    """
    #parent.destroy()
    user_name = e1.get()
    # 核对是否注册过
    print('check_info user name :', user_name)
    try:
        with open("dataset/users_info_dic.pkl", "rb") as tf:
            users_info_dic = pickle.load(tf)
    except:
        users_info_dic = dict()
    tf.close()
    # 没注册过，跳到注册界面
    if user_name not in users_info_dic.keys():
        need_save_info = True
        # askyesno返回True False, askquestion返回“Yes" ”No“
        tmp = tkinter.messagebox.askyesno(message='You have not registered yet\nDo you want to register?')
        if tmp == False:
            return
        else:
            sign_up(need_save_info, parent)
        """
        check_info_error = Tk()
        check_info_error.title('error')
        check_info_error.geometry("350x200+400+200")
        Label(check_info_error, text='\n  ERROR!\n\n   You have not registered yet.',
              font="微软雅黑 14").grid(row=0, column=0, columnspan=2, sticky="w", pady=10)
        Button(check_info_error, text='sign up!', font="宋体 14", relief="raised",
           command=lambda: sign_up(need_save_info, check_info_error)).grid(row=1, column=0, columnspan=2, pady=20)
        #check_info_error.destroy()
        parent.destroy()
        """
        print('Error, you have not registered yet.')
    # 登录成功，跳到查询界面
    else:
        # parent.destroy()
        # check_info_suc = Tk()
        # check_info_suc.title('Login success')
        tkinter.messagebox.showinfo(message="Login success.")
        login_jump_query(e1, parent)
        #query(flag = False, user_name = e1, user_age = None, user_sex = None, parent = parent)
        # 登录日志
        now_time = str(datetime.datetime.now())[0:-7]
        query_log = '[' + now_time + '] ' + 'OP: log_in, ' + 'user_name:@' + user_name + '\n'
        with open("dataset/query_record_log.txt", "a", encoding='utf-8') as f:
            f.write(query_log)
        f.close()
        print('Login success, ', user_name, '!')
        print('@ write user login information log over.')
        # 获取全局变量用户年龄
        global global_age
        global_age = users_info_dic[user_name].age


def log_in(parent):
    """
    登录界面，输入用户名
    :param parent:
    :return:
    """
    parent.destroy()
    login = Tk()
    login.title("log in")
    login.geometry("350x200+400+200")

    user_name = Entry(login, width=30)#, textvariable = V_name)
    # pwdE = Entry(login, width=30)
    Label(login, text='\nEnter user name:\n', font="微软雅黑 14").grid(row=0, column=0, columnspan=2, sticky="w",
                                                 pady=10)
    user_name.grid(row=1, column=1, sticky="e", padx=20)

    # login.mainloop()
    # user_name_str = V_name.get()
    # print('log in user_name_str:',user_name_str)
    Button(login, text="log in", font="宋体 14", relief="raised",
           command=lambda: check_info(user_name, login)).grid(row=3,column=0, columnspan=2,pady=20)


if __name__ == '__main__':
    # my_user_term = log_in_v1()
    # to_query()
    try:
        with open("dataset/users_info_dic.pkl", "rb") as tf:
            users_info_dic = pickle.load(tf)
    except:
        users_info_dic = dict()
    # 主页面
    master = Tk()
    master.title("welcome")
    # 宽420 高400
    master.geometry("460x250+400+200")

    Label(master,text='\nUse 2012679 web search engine.\n\nSearch for news links for you.\n\n''Based on http://news.nankai.edu.cn.\n',
        font="楷体 17", justify=LEFT).grid(row=1, column=0, columnspan=2,
                                         sticky='w', pady=10)
    # 登录
    Button(master, text="log in", font="楷体 14", relief="raised", command=lambda: log_in(master)).grid(row=4, column=0, pady=5)
    # 注册
    Button(master, text="sign up", font="楷体 14", relief="raised", command=lambda: sign_up(flag=True, parent=master)).grid(row=4, column=1)
    master.mainloop()



