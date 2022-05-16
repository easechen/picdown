import requests
from lxml import etree
import time
import os

localPath = os.getcwd()+'/downloads'
head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36','Referer':'https://www.meitu131.net/'}


def getHtml(start_url, encode):
    r = requests.get(start_url, headers=head)
    r.encoding = encode
    html = etree.HTML(r.text)
    return html

def downPic(name, src, path):
    r = requests.get(src, headers=head)
    path = path+str(name)+".jpg"
    fp = open(path, 'wb')
    fp.write(r.content)
    fp.close()


def get_full_nl(url, nl):
    index = nl.rfind("/")
    if index == -1:
        full_url = url[:url.rfind("/")+1] + nl
    else:
        full_url = url[:url.rfind("/")] + nl[index:]
        
    return full_url

def downSeries(start_series_url, encode, name_xpath_str, pic_xpath_str, next_page_xpath_str):
    html = getHtml(start_series_url, encode)
    # 文件夹名称
    dirname = html.xpath(name_xpath_str)[0]
    dir_path = localPath+'/'+dirname+'/'
    # create dir
    if os.path.exists(dir_path):
        pass
    else:
        os.makedirs(dir_path)
    os.startfile(dir_path)
    i = 0
    while True:
        pic_url = html.xpath(pic_xpath_str)[0]
        downPic(i, pic_url, dir_path)
        print(f"下载成功，{i}")
        i += 1
        nl = html.xpath(next_page_xpath_str)[0]
        if nl[-4:] != 'html':
            break
        else:
            next_url =  get_full_nl(start_series_url, nl)
            html = getHtml(next_url, encode)

def down(select, url):
    if select == '1':
        name_xpath_str = '//h1/text()'
        pic_xpath_str = '//a[@class="down-btn"]/@href'
        next_page_xpath_str = '//li[@id="nl"]/a/@href'
        encode = "GBK"
    elif select == '2':
        name_xpath_str = '//div[@class="work-content"]/p/a/img/@alt' 
        pic_xpath_str = '//div[@class="work-content"]/p/a/img/@src'
        next_page_xpath_str = '//div[@class="work-content"]/p/a/@href'
        encode = "utf-8"
    downSeries(url, encode, name_xpath_str, pic_xpath_str, next_page_xpath_str)


if __name__=='__main__':
    # name_xpath_str = '//h1/text()'
    # pic_xpath_str = '//a[@class="down-btn"]/@href'
    # next_page_xpath_str = '//li[@id="nl"]/a/@href'
    select = input("1、唯一图库 2、meitu131\n:")
    if select == '1':
        name_xpath_str = '//h1/text()'
        pic_xpath_str = '//a[@class="down-btn"]/@href'
        next_page_xpath_str = '//li[@id="nl"]/a/@href'
        encode = "GBK"
    elif select == '2':
        name_xpath_str = '//div[@class="work-content"]/p/a/img/@alt' 
        pic_xpath_str = '//div[@class="work-content"]/p/a/img/@src'
        next_page_xpath_str = '//div[@class="work-content"]/p/a/@href'
        encode = "utf-8"
 
    print(localPath)

    url = input("enter url:")

    downSeries(url, encode, name_xpath_str, pic_xpath_str, next_page_xpath_str)

    input("任意键退出")
