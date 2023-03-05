import requests
import os
import bs4
import time
from bs4 import BeautifulSoup
import re


def filter_str(desstr, restr=''):
    # 过滤除中英文及数字以外的其他字符
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
    return res.sub(restr, desstr)


pa = input("1 從最新開始 2 自訂")
if pa == '1':
    url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
    href_x = 100000
elif pa == '2':
    start = int(input("從哪一頁開始"))
    url = 'https://www.ptt.cc/bbs/Gossiping/index{}.html'.format(start)
    href_x = start
end = int(input("到哪一頁結束"))
cookies = {"over18": '1'}

web = requests.get(url, cookies=cookies)
soup = BeautifulSoup(web.text, "html.parser")
tmp = soup.find_all('div', class_='r-ent')
last = soup.find_all('a', class_='btn wide')
# main-container > div.r-list-container.action-bar-margin.bbs-screen > div:nth-child(10)
cnt = 0
#string = '["'
now = time.localtime(time.time())
if int(now.tm_mday) < 10:  # 11/01!=11/1
    string_date = str(now.tm_mon)+'/0'+str(now.tm_mday)
else:
    string_date = str(now.tm_mon)+'/'+str(now.tm_mday)
string_date2 = str(now.tm_mon)+'_'+str(now.tm_mday)  # 存txt名稱
string_hour = str(now.tm_hour)

string_minute = str(now.tm_min)
print(string_date)

while True:
    notoday = 0
    for i in tmp:
        string = ""
        output = open("C:\\guanlinpy\\temp\\test\\test.txt",
                      "a", encoding="utf-8")
        meta = i.find('div', class_='meta')
        date = meta.find('div', class_='date')
        weight = i.find('div', class_='nrec')  # 權重weight.text
    #    print(weight.text)
        # print(date.text)
        date_int = int(date.text.replace('/', ''))

        # if(date.text!=string_date):#判斷是否今日
        #   notoday+=1
        #   continue

       # if(date_int<=1000):
        #    notoday+=1
        #   continue
        if(href_x <= end):
            notoday += 1
            continue

        author = i.find('div', class_='title')
        author_empty = author.text.split()
        if(author_empty[0][0] == "("):
            continue
        web = author.a['href']

        title = author.a.text

        url = 'https://www.ptt.cc' + web

        try:
            web = requests.get(url, cookies=cookies)
        except:
            print("time out")

        soup = BeautifulSoup(web.text, "html.parser")
        tmp = soup.find('div', id="main-content")

        try:
            all_text = tmp.text
        except:
            print('此篇被刪除')
            continue

        a = all_text.split(url)[0]  # 內文
#        b =all_text.split(url)[1]#留言

        cnt += 1

        string += title+'\n'+a+'\n\n'

        string += a

        string = string.replace('\n', '').replace('\t', '').replace(' ', '')
        string += '",'+'\n'+'"'
        output.write(string)
        output.close()
        try:
            os.mkdir("C:\\guanlinpy\\temp")
        except FileExistsError:
            pass
    if(notoday >= 19):
        break

    scr = 'https://www.ptt.cc'+last[1]['href']  # 上頁
    href_x = int(scr[38:43])

    print(last[1]['href'])
    web = requests.get(scr, cookies=cookies)
    soup = BeautifulSoup(web.text, "html.parser")
    tmp = soup.find_all('div', class_='r-ent')
    last = soup.find_all('a', class_='btn wide')


# x=string.rfind('","')
# string1=string[0:x]
# string1+='"]'
#file_name = "ptt_"+string_date2
#output = open("test.txt", "w",encoding="utf-8")
#output = open("./temp/" + file_name + ".txt", "w",encoding="utf-8")
# output.write(string1)
output.close()
