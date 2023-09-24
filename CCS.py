#功能
#文章tile和作者信息
#摘要

import requests
import json
import os
import time
from bs4 import BeautifulSoup
import bs4
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#该函数获取历年会议的url，格式如下
# {'history': 'https://www.sigsac.org/ccs/ccs-history.html', ' 2023': 'http://www.sigsac.org/ccs/CCS2023', 
#  ' 2022': 'http://www.sigsac.org/ccs/CCS2022', ' 2021': 'http://www.sigsac.org/ccs/CCS2021', 
#  ' 2020': 'http://www.sigsac.org/ccs/CCS2020', ' 2019': 'http://www.sigsac.org/ccs/CCS2019', 
#  ' 2018': 'http://www.sigsac.org/ccs/CCS2018', ' 2017': 'http://www.sigsac.org/ccs/CCS2017', 
#  ' 2016': 'http://www.sigsac.org/ccs/CCS2016', ' 2015': 'http://www.sigsac.org/ccs/CCS2015', 
#  ' 2014': 'http://www.sigsac.org/ccs/CCS2014', ' 2013': 'http://www.sigsac.org/ccs/CCS2013', 
#  ' 2012': 'http://www.sigsac.org/ccs/CCS2012', ' 2011': 'http://www.sigsac.org/ccs/CCS2011', 
#  ' 2010': 'http://www.sigsac.org/ccs/CCS2010', ' 2009': 'http://www.sigsac.org/ccs/CCS2009', 
#  ' 2008': 'http://www.sigsac.org/ccs/CCS2008', ' 2007': 'http://www.sigsac.org/ccs/CCS2007', 
#  ' 2006': 'http://www.sigsac.org/ccs/CCS2006', ' 2005': 'http://www.sigsac.org/ccs/CCS2005', 
#  ' 2004': 'http://www.sigsac.org/ccs/CCS2004', ' 2003': '未公开', ' 2002': '未公开', 
#  ' 2001': '未公开', ' 2000': '未公开', ' 1999': '未公开', ' 1998': '未公开', ' 1997': '未公开', 
#  ' 1996': '未公开', ' 1994': '未公开', ' 1993': '未公开'}
#获取ccs历年会议的url
def get_history_urls():
    urls = {'history': "https://www.sigsac.org/ccs/ccs-history.html"}
    url = urls['history']
    response = requests.get(url, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    conferences = soup.find_all('li')
    for conference in conferences:
        tag_a= conference.find_all('a')[0]
        href = tag_a.find_all('a')[0].get("href") if len(tag_a.find_all('a')) else "未公开"
        year = conference.find_all(string=True, recursive=False)[1].strip().split(',')[1].strip()
        urls[year] = href
    return urls

#如果文件超过一个月没有更新，那就更新url保存到文件里面
def update_urls():
    if os.path.exists('./CCS_history_urls.txt'):
        last_time = os.path.getmtime('./CCS_history_urls.txt')
        now = time.time()
        if now - last_time > 30 * 24 * 60 * 60:
            urls = get_history_urls()
            with open("./CCS_history_urls.txt", "w") as f:
                json.dump(urls, f)
    else:
        with open("./CCS_history_urls.txt", "w") as f:
            urls = get_history_urls()
            json.dump(urls, f)
    
#获取year年的论文列表
def get_papers(year):
    urls = {}
    with open("./CCS_history_urls.txt", "r") as f:
        content = f.read()
        # 将字符串转换为字典
        urls = eval(content)
    url = urls[year]
    paper_url = url + "/accepted-papers.html"
    if year == "2022":
        paper_url = "https://www.sigsac.org/ccs/CCS2022/program/accepted-papers.html"
    response = requests.get(paper_url, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    papers = soup.find_all('b')
    papers = list(map(lambda x: x.get_text(), papers))
    papers = list(map(lambda x: x.lower(), papers))
    return papers

#查找关键字
def match_key_words(papers, key):
    result = []
    key = key.lower()
    for paper in papers:
        if key in paper:
            result.append(paper)
    return result

#获取title的摘要
def get_abstract(title):
    print(title)
    params = {"fillQuickSearch":"false","target":"advanced","expand":"dl","field1":"AllField","text1":title}
    response = requests.get('https://dl.acm.org/action/doSearch', params=params,verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    paper_url = "https://dl.acm.org" + soup.find(name="span", attrs={"class" :"hlFld-Title"}).contents[0]['href']
    response = requests.get(paper_url,verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    abstracts = soup.find(attrs={"class" :"article__section article__abstract hlFld-Abstract"}).contents[1]
    abstract = ""
    for i in abstracts:
        if type(i) == bs4.element.Tag:
            if i.name == 'p':
                abstract = abstract + i.text + "\n"
    return {title: abstract}

#获取titles的摘要
def get_abstracts(titles):
    ans = {}
    for title in titles:
        tmp = get_abstract(title)
        ans.update(tmp)
    return ans

