import requests
import json
import os
import time
from bs4 import BeautifulSoup
import bs4
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://www.ndss-symposium.org/"

def get_url(year):
    year = int(year)
    if year > 2022 :
        url = "https://sp" + str(year) + ".ieee-security.org/program-papers.html"
    else:
        url = "https://www.ieee-security.org/TC/SP" + str(year) + "/program-papers.html"
    return url

def get_papers(year):
    url = get_url(year)
    response = requests.get(url, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    papers = soup.find_all(attrs={"class" :"list-group-item"})
    titles = []
    for paper in papers:
        title = paper.contents[1].text.strip().lower()
        titles.append(title)
    abstracts = soup.find_all(attrs={"class" :"panel-collapse collapse"})
    abs = []
    if abstracts != None:
        for abstract in abstracts:
            a = abstract.contents[1].contents[0].text.strip()
            abs.append(a)

    abstracts = dict(zip(titles, abs))
    return [titles, abstracts]

def match_key_words(papers, key):
    result = []
    key = key.lower()
    for paper in papers:
        if key in paper:
            result.append(paper)
    return result