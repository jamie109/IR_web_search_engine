from tkinter import *




if __name__ == '__main__':
    # 主页面
    master = Tk()
    master.title("welcome")
    #宽420 高400 第1个加号是距离屏幕左边的宽，第2个加号是距离屏幕顶部的高
    #master.geometry("420x200+500+200")
    master.geometry("460x250+400+200")
    Label(text='\nUse jamie109 web search engine.\n\nSearch for news links for you.\n\nBased on http://news.nankai.edu.cn.\n',
          font="楷体 17", justify=LEFT).grid(row=1, column=0, columnspan=2,
                                           sticky='w', pady=10)
    # Label(text="您好!\n""欢迎登录学生选课系统\n""温馨提示：\n""初始密码为学号，初次登录请修改密码\n",
    #       font="楷体 17", justify=LEFT).grid(row=1, column=0, columnspan=2,sticky='w', pady=10)
    # 登录
    Button(master, text="log in", font="楷体 14", relief="raised", ).grid(row=4, column=0, pady=5)
    # 注册
    Button(master, text="sign up", font="楷体 14", relief="raised").grid(row=4, column=1)
    master.mainloop()