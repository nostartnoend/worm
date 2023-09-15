import requests
import re
import bs4
import os
import json
import urllib.parse
from tkinter import *
import sys

#难度列表
dl= ["暂无评定","入门","普及-","普及和提高-","普及+和提高","提高+和省选-","省选和NOI-","NOI和NOI+和CTSC"]
#难度网页码
dll=[0,1,2,3,4,5,6,7]
#题库类型
tiku= ["洛谷","主题库","入门与考试","CodeForces","SPOJ","AtCoder" ,"UVA"]
#题库网页码
tikucode=["B%7CP","P","B","CF","SP","AT","UVA"]
#获取网页源码
url="https://www.luogu.com.cn/problem/"
def test(a):
    print(a)
def kaishipaxing(url1,url2,dif,tik,key):
  headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36","cookie":"__client_id=65dc4916409c789c9e15de31ec9f8cc29cbffad8; _uid=643508"
  }
  response=requests.get(url=url2 ,headers= headers)
  response.encoding="utf-8"
  #获取每道题的href数据
  problemhref=re.findall('<a href="(.*?)">.*?',response.text)
  #依次访问每道题的网址，网址为url+href
  for i in problemhref:
    #爬虫结果文件夹
    if not os.path.exists("爬虫结果"):
        os.mkdir("爬虫结果")
    p_url=url1+i
    p_response=requests.get(url=p_url,headers= headers)
    p_response.encoding="utf-8"
    #获取题目的标题
    problemtitle = re.findall('<h1>(.*?)</h1>', p_response.text)
    #获取网页的markdown源码
    p_soup = bs4.BeautifulSoup(p_response.text, "html.parser")
    core = p_soup.select("article")[0]
    md = str(core)
    md = re.sub("<h1>", "# ", md)
    md = re.sub("<h2>", "## ", md)
    md = re.sub("<h3>", "#### ", md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
    #判断是否有同名文件夹
    if not os.path.exists("爬虫结果/"+i+"-"+problemtitle[0]):
        os.mkdir("爬虫结果/"+i+"-"+problemtitle[0])
    #将md保存到一个文件中，文件保存在之前创建的文件夹内
    with open("爬虫结果/"+i+"-"+problemtitle[0]+"/"+i+"-"+problemtitle[0]+".md","w",encoding="utf-8") as f:
        f.write(md)
    #如果文件保存成功，则输出 题号-题目正在爬取 的信息，如果失败，则输出 题号-题目爬取失败 的信息
    if os.path.exists("爬虫结果/"+i+"-"+problemtitle[0]+"/"+i+"-"+problemtitle[0]+".md"):
        print(i+"-"+problemtitle[0]+"正在爬取")
    else:
        print(i+"-"+problemtitle[0]+"爬取失败")
    #进行题解的访问
    ps_url=url1+"/solution/"+i
    ps_response=requests.get(url=ps_url,headers= headers)
    #改变格式
    decoded_uri_component = str(urllib.parse.unquote(ps_response.text, encoding='unicode_escape', errors='replace'))
    result_index = decoded_uri_component.find("content\":\"")
    # 去掉多余的符号
    result_index += 10;
    decoded_uri_component = decoded_uri_component[result_index:]
    final_index = decoded_uri_component.find("type")
    # 去掉多余的符号
    final_index -= 6
    decoded_uri_component = decoded_uri_component[:final_index]
    #获取题解的markdown源码
    ps_soup = bs4.BeautifulSoup(ps_response.text, "html.parser")
    ps_core = ps_soup.select_one("script")
    ps_md = str( decoded_uri_component)
    ps_md = re.sub("<h1>", "# ", ps_md)
    ps_md = re.sub("<h2>", "## ", ps_md)
    ps_md = re.sub("<h3>", "#### ", ps_md)
    ps_md = re.sub("</?[a-zA-Z]+[^<>]*>", "", ps_md)
    #将题解保存到一个文件中，文件保存在之前创建的文件夹内
    with open("爬虫结果/"+i+"-"+problemtitle[0]+"/"+i+"-"+problemtitle[0]+"-题解.md","w",encoding="utf-8") as f:
        f.write(ps_md)
    #如果文件保存成功，则在控制台输出 题号-题目已成功爬取 的信息，如果失败，则输出 题号-题目爬取失败 的信息
    if os.path.exists("爬虫结果/"+i+"-"+problemtitle[0]+"/"+i+"-"+problemtitle[0]+".md"):
        print(i+"-"+problemtitle[0]+"已成功爬取")
    else:
        print(i+"-"+problemtitle[0]+"爬取失败")
    if os.path.exists("爬虫结果/"+i+"-"+problemtitle[0]+"/"+i+"-"+problemtitle[0]+"-题解.md"):
        print(i+"-"+problemtitle[0]+"-题解已成功爬取")
    else:
        print(i+"-"+problemtitle[0]+"-题解爬取失败")

 #用tkinter创建一个窗口
 #窗口包含两个下拉菜单用于选取dl列表内的难度和tiku列表内的题库类型，一个输入窗口用于输入关键词，一个按钮用于开始爬行
 #点击按钮后，调用kaishipaxing函数,将选取的难度，题库类型，关键词作为dif，tik，key传入
def CreatW():
    root = Tk()
    root.title("洛谷题目爬虫")
    root.geometry('500x300')
    root.resizable(width=False, height=False)
    #创建一个label用于显示难度
    label1 = Label(root, text="难度：")
    label1.grid(row=0, column=0, sticky=W)
    #创建一个label用于显示题库
    label2 = Label(root, text="题库：")
    label2.grid(row=0, column=2, sticky=W)
    #创建一个label用于显示关键词
    label3 = Label(root, text="关键词：")
    label3.grid(row=1, column=0, sticky=W)
    #创建一个下拉菜单用于选择难度
    var1 = StringVar()
    var1.set(dl[0])
    option1 = OptionMenu(root, var1, *dl)
    option1.grid(row=0, column=1, sticky=W)
    #创建一个下拉菜单用于选择题库
    var2 = StringVar()
    var2.set(tiku[0])
    option2 = OptionMenu(root, var2, *tiku)
    option2.grid(row=0, column=3, sticky=W)
    #创建一个输入框用于输入关键词
    entry1 = Entry(root)
    entry1.grid(row=1, column=1, sticky=W)
    #创建一个按钮用于开始爬行
    button1 = Button(root, text="开始爬行", command=lambda: kaishipaxing(url,url + "list?"+"difficulty="+str(dll[dl.index(var1.get())])+ "&keyword=" + entry1.get()+"&type="+tikucode[tiku.index(var2.get())] + "&page=1", dll[dl.index(var1.get())], tiku[tiku.index(var2.get())], entry1.get()))
    button1.grid(row=2, column=1, sticky=W)
    #在窗口中下创建一个不会影响其他组件的小窗口显示控制台的滚动信息
    text = Text(root, width=60, height=10)
    text.grid(row=3, columnspan=4)
    #重定向输出，将控制台的输出重定向到text中
    sys.stdout = StdoutRedirector(text)
    root.mainloop()
class StdoutRedirector(object):
        def __init__(self, text_widget):
            self.text_space = text_widget

        def write(self, string):
            self.text_space.insert('end', string)
            self.text_space.see('end')
            self.text_space.update_idletasks()
if __name__ == '__main__':
    CreatW()






 # See PyCharm help at https://www.jetbrains.com/help/pycharm/
