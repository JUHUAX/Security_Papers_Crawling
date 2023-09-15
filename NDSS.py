import requests
import json
import os
import time
from bs4 import BeautifulSoup
import bs4


base_url = "https://www.ndss-symposium.org/"

def get_hrefs(year):
    index = "ndss" + str(year) + "/accepted-papers/"
    url = base_url + index
    response = requests.get(url, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    hrefs = soup.find_all(attrs={"class" :"paper-link-abs"})
    return hrefs

def get_papers(year):
    hrefs = get_hrefs(year)
    titles = []
    abstracts = []
    pdfs = []
    for href in hrefs:
        url = href['href']
        response = requests.get(url, verify=False)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find_all(attrs={"class" :"entry-title"})[0].text.lower()
        titles.append(title)
        abstract = soup.find_all(attrs={"class" :"paper-data"})[0].contents[3].text.lower()
        abstracts.append(abstract)
        pdf = soup.find_all(attrs={"class" :"btn btn-light btn-sm pdf-button"})[0]['href']
        pdfs.append(pdf)
    titles_abstracts = dict(zip(titles, abstracts))
    titles_pdfs = dict(zip(titles, pdfs))
    return [titles, titles_abstracts, titles_pdfs]

def match_key_words(papers, key):
    result = []
    key = key.lower()
    for paper in papers:
        if key in paper:
            result.append(paper)
    return result

print(match_key_words(get_papers(2022)[0], "fuzz"))