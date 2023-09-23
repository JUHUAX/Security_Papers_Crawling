import os, time, argparse, json
from CCS import get_papers as CCS_get_papers
from CCS import update_urls
from CCS import get_abstract as CCS_get_abstract
from NDSS import get_papers as NDSS_get_papers
from USENIX import get_papers as USENIX_get_papers
from USENIX import get_pdf as USENIX_get_pdf
from SP import get_papers as SP_get_papers

def update_papers(path):
    if os.path.exists(path):
        last_time = os.path.getmtime(path)
        now = time.time()
        if now - last_time < 30 * 24 * 60 * 60:
            return False
    return True

def load_papers(path):
    with open(path, "r") as f:
        content = f.read()
        # 将字符串转换为字典
        return eval(content)
    
def match_key_words(papers, key):
    result = []
    key = key.lower()
    for paper in papers:
        if key in paper:
            result.append(paper)
    return result


# CCS
def update_CCS(year):
    path0 = "./contents/CCS-" + year + "-papers.txt"
    path1 = "./contents/CCS-" + year + "-papers&abstracts.txt"
    #更新papers&abstract文件操作
    if update_papers(path0):
        papers = CCS_get_papers(year)
        with open(path0, "w") as f:
                json.dump(papers, f)
        results = {}
        for paper in papers:
            result = CCS_get_abstract(paper) #{paper_title: abstract}
            results.update(result)
        with open(path1, "w") as f:
                json.dump(results, f)

def get_CCS(year, keyword):
    update_CCS(year)
    path = "./contents/CCS-" + year + "-papers&abstracts.txt"
    results = load_papers(path)
    papers = list(results)
    if keyword != None:
        papers = match_key_words(papers, keyword)
    for paper in papers:
        print("论文题目：" + paper)
        print("")
        print("论文摘要：" + results[paper])
        print("--------------------------------------------------------------------------------------------------------------------------")

# NDSS
def update_NDSS(year):
    path0 = "./contents/NDSS-" + year + "-papers.txt"
    path1 = "./contents/NDSS-" + year + "-papers&abstracts.txt"
    path2 = "./contents/NDSS-" + year + "-papers&pdfs.txt"
    #更新papers&abstract文件操作
    if update_papers(path1):
        contents = NDSS_get_papers(year)
        with open(path0, "w") as f:
            json.dump(contents[0], f)
        with open(path1, "w") as f:
            json.dump(contents[1], f)
        with open(path2, "w") as f:
            json.dump(contents[2], f)

def get_NDSS(year, keyword):
    update_NDSS(year)
    path0 = "./contents/NDSS-" + year + "-papers.txt"
    path1 = "./contents/NDSS-" + year + "-papers&abstracts.txt"
    path2 = "./contents/NDSS-" + year + "-papers&pdfs.txt"
    with open(path0, "r") as f:
        papers = f.read()
        papers = json.loads(papers)
    abstracts = load_papers(path1)
    pdfs = load_papers(path2)
    if keyword != None:
        papers = match_key_words(papers, keyword)
    for paper in papers:
        print("论文题目：" + paper)
        print("")
        print("论文摘要：" + abstracts[paper])
        print("")
        print("论文pdf：" + pdfs[paper])
        print("---------------------------------------------------------------------------------------------------------------")


# USENIX
def update_USENIX(year):
    path0 = "./contents/USENIX-" + year + "-papers.txt"
    path1 = "./contents/USENIX-" + year + "-papers&abstracts.txt"
    path2 = "./contents/USENIX-" + year + "-papers&urls.txt"
    #更新papers&abstract文件操作
    if update_papers(path1):
        contents = USENIX_get_papers(year)
        with open(path0, "w") as f:
            json.dump(contents[0], f)
        with open(path1, "w") as f:
            json.dump(contents[2], f)
        with open(path2, "w") as f:
            json.dump(contents[1], f)

def get_USENIX(year, keyword):
    update_USENIX(year)
    path0 = "./contents/USENIX-" + year + "-papers.txt"
    path1 = "./contents/USENIX-" + year + "-papers&abstracts.txt"
    path2 = "./contents/USENIX-" + year + "-papers&urls.txt"
    with open(path0, "r") as f:
        papers = f.read()
        papers = json.loads(papers)
    abstracts = load_papers(path1)
    urls = load_papers(path2)
    if keyword != None:
        papers = match_key_words(papers, keyword)
    for paper in papers:
        print("论文题目：" + paper)
        print("")
        print("论文摘要：" + abstracts[paper])
        print("")
        print("论文pdf：" + urls[paper])
        print("---------------------------------------------------------------------------------------------------------------")

# SP
def update_SP(year):
    path = "./contents/SP-" + year + "-papers.txt"
    #更新papers&abstract文件操作
    if update_papers(path):
        contents = SP_get_papers(year)
        with open(path, "w") as f:
            json.dump(contents, f)

def get_SP(year, keyword):
    update_SP(year)
    path = "./contents/SP-" + year + "-papers.txt"
    with open(path, "r") as f:
        papers = f.read()
        papers = json.loads(papers)
    if keyword != None:
        papers = match_key_words(papers, keyword)
    for paper in papers:
        print("论文题目：" + paper)
        print("---------------------------------------------------------------------------------------------------------------")

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--conference', help='会议名称', required=True)
parser.add_argument('-y', '--year', help='年份', required=True)
parser.add_argument('-k', '--keyword', help='关键字')
parser.add_argument('-a', '--abstract', help='摘要')
parser.add_argument('-l', '--link', help='链接')

args = parser.parse_args()
conference = args.conference
year = args.year
keyword = args.keyword

if conference == "CCS":
    get_CCS(year, keyword)

if conference == "USENIX":
    get_USENIX(year, keyword)

if conference == "SP":
    get_SP(year, keyword)

if conference == "NDSS":
    get_NDSS(year, keyword)
