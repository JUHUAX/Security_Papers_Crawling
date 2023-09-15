import requests
from bs4 import BeautifulSoup

def get_papers_by_url(url):
    response = requests.get(url, verify=False)
    if response.status_code == 404:
        return [[], {}, {}]
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    papers = []
    papers_urls = []
    papers_abstracts = []
    titles = soup.find_all(attrs={"class" :"node-title"})
    abstracts = soup.find_all(attrs={"class" :"content"})
    for title in titles[1:]:
        papers.append(title.contents[1].text.lower())
        papers_urls.append("https://www.usenix.org/" + title.contents[1]['href'])
    
    for i in range(4,len(abstracts)-1):
        p_lables = abstracts[i].contents[1].contents[2].contents[0].contents
        abstract = ""
        for p in p_lables:
            abstract = abstract + p.text + "\n"
        papers_abstracts.append(abstract)
    
    papers_urls = dict(zip(papers, papers_urls))
    papers_abstracts = dict(zip(papers, papers_abstracts))
    return [papers, papers_urls, papers_abstracts]
    #papers 是论文名的列表
    #papers_urls是论文名+url的字典
    #papers_abstracts是论文名+摘要的字典

def get_papers(year):
    index = int(year) - 2000
    base_url = "https://www.usenix.org/conference/usenixsecurity"
    conference_url = base_url + str(index)
    winter = "/winter-accepted-papers"
    summer = "/summer-accepted-papers"
    fall = "/fall-accepted-papers"
    
    summer = get_papers_by_url(conference_url + summer)
    fall = get_papers_by_url(conference_url + fall)
    winter = get_papers_by_url(conference_url + winter)
    papers = summer[0] + fall[0] + winter[0]
    summer[1].update(fall[1])
    summer[1].update(winter[1])
    papers_urls = summer[1]
    summer[2].update(fall[2])
    summer[2].update(winter[2])
    papers_abstracts = summer[2]
    # print(len(papers))
    # print(len(papers_urls))
    # print(len(papers_abstracts))
    return [papers, papers_urls, papers_abstracts]

def match_key_words(papers, key):
    result = []
    key = key.lower()
    for paper in papers:
        if key in paper:
            result.append(paper)
    return result

def get_pdf(url):
    response = requests.get(url, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    url = soup.find_all(attrs={"class" :"file"})[1].contents[2]['href']
    # print(url)
    return url