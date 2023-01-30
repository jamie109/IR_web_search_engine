## Web搜索引擎 （期末⼤作业）
## 建议退课！ 建议退课！ 建议退课！ 
### 食用指南
1. 先运行spider.py，获取网页内容。

   * 可自行更改`cc_base_url = 'http://cc.nankai.edu.cn'`和`to_use_url_list = ['http://cc.nankai.edu.cn']`中的链接。
   这是你要爬取的网页，可以改成南开电光学院、人工智能学院等等。
   * `if to_use_url_list is not None and mycount < 50`中mycount小于多少可以自定义，这是你想要爬取的网页数目。
   * `sleep(random.randint(2, 3))`中的2和3也可以更改，这是爬完一个网页等待一会儿的时间，谓之”爬虫礼仪也“。（去掉这行代码会快一些。）


### 实验要求和实现思路
#### 1. ⽹⻚抓取(10%) 2023.1.30 finish
##### 要求

根据搜索引擎主题选择⽹站进⾏爬取，爬取⽹⻚数⽬不限制，注意不要违法，主题不会作为评分标准，不需要太过纠结爬什么。

##### 思路

* 爬取流程
   * 准备
  
   首先需要一个集合`used_url_set`记录已经爬取过的网页，一个列表`to_use_url_list`记录将要爬取的网页。
   初始时`used_url_set`为空，`to_use_url_list`中只有一个网页A。

   * 爬取A 
  
   A的标题，去掉符号，作为存储相关数据（html、文本内容等）的文件名。 
   html文件存到dataset/html_data文件夹下面。 
   该网页的url（例如http://cc.nankai.edu.cn，存到第一行）和文本内容（存到第二行）存在dataset/web_data文件夹下面。
   其命名为'_数字_去掉了标点符号的网页标题.html/txt'，数字表示这是第几个爬取的网页。

   A中可能会有很多跳转到其他地方的链接BCD等等，如果以前没有爬过（它们不在`used_url_set`中），要把它们加到`to_use_url_list`中。

   * 爬完A
  
   把A从`to_use_url_list`删掉，加到`used_url_set`中。
   接着，如果`to_use_url_list`不为空，就从中选取一个url接着爬，我用的是第0个。


