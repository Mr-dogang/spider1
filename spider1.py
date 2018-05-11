# -*- coding: utf-8 -*-
import requests,re,os,time
from bs4 import BeautifulSoup
from multiprocessing import Pool


#def noval_url():


def get_novel_info(url):
    chapter_url = list()
    chapter_name = list()
    info = {}
    chapter_html = requests.get(url,params = header)
    chapter_html.encoding = 'gbk'
    chapter_html = BeautifulSoup(chapter_html.text,"html.parser")
    #print(bsObj)
    chapter_urls = chapter_html.select('.main .chapterlist ul li a')
    info['novel_name'] = chapter_html.select('.main .articleinfo .r .l2 .p1 h1')[0].get_text()
    info['novel_author'] = chapter_html.select('.main .articleinfo .r .l2 .p1 span')[0].get_text()
    info['novel_abstract'] = chapter_html.select('.main .articleinfo .r .l2 .p3')[0].get_text()
    for cu in chapter_urls:
        chapter_name.append(cu.get_text())
        cu = cu['href']
        chapter_url.append(cu)
    #print(chapter_url)
    
    return chapter_url,chapter_name,info


def get_noval_text(html,url):
    html = requests.get(html+url,params = header)
    html.encoding = 'gbk'
    bsObj = BeautifulSoup(html.text,"html.parser")
    #print(bsObj)
    #chapter_name = bsObj.select('.main h1')[0].get_text()
    #print(chapter_name)
    chapter_text = bsObj.select('.main .content p')[0].get_text('\n   ','<br/>')
    #print(chapter_text)
    return chapter_text
    

def write_text(chapter_urls,chapter_names,novel_info):
    chapter_num = len(chapter_urls)
    finish_num = 0
    with open('G:\学习\github\learning\spider1\《{0}》.txt'.format(novel_info['novel_name']),'w',encoding='utf') as f:
        f.write('《'+novel_info['novel_name']+'》\n')
        f.write(novel_info['novel_author']+'\n\n')
        if novel_info['novel_abstract'] != '':
            f.write('简介：\n'+novel_info['novel_abstract']+'\n\n')
        else:
            f.write('简介：无'+'\n\n')
        for i in range(chapter_num):
            try:
                chapter_text = get_noval_text(html,chapter_urls[i])
            except IndexError:
                noval_text = '此章服务器端丢失！敬请谅解！'
            #noval_names.append(noval_name)
            #noval_texts.append(noval_text)
            f.write(chapter_names[i]+'\n')
            f.write('   '+chapter_text+'\n\n')
            finish_num += 1
            print('请稍候，正在下载：'+chapter_names[i]+' 进度：'+str(finish_num)+'/'+str(chapter_num))
    

if __name__ == '__main__':
    start = time.clock()
    html = "http://www.tsxsw.com/html/49/49678/"
    header = {
    'Host': 'www.tsxsw.com',
    'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
          }
    chapter_urls,chapter_names,novel_info = get_novel_info(html)
    print('正在为您下载：《'+novel_info['novel_name']+'》请稍等……')
    start_download = write_text(chapter_urls, chapter_names, novel_info)
    end = time.clock()
    print('亲~总共用了：'+str(end-start)+'秒 \n您的小说已经下载完成了哦~敬请享用吧~(#^.^#)~')

    
