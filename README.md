# Security_Papers_Crawling
## Introduction
In this repo, we realize a crawler to crawl papers in S&P/CCS/USENIX Security/NDSS for reading papers in the security field according to the given keywords.

在本仓库，我们实现了一个根据给定关键词来爬取安全四大会论文的爬虫。

## Motivation
To our best knowledge, among existing crawlers in github, none has realized crawling papers according to the keywords, which makes screening papers still time-consuming.

我没找到现有可以实现根据关键词爬取论文的爬虫，就很烦，就自己实现一个。

## Implement
python3 spider.py [-c --conference] [-y --year] [-K --keywords]

example: **python spider.py -c CCS -y 2022 -k fuzz**

necessary arguments:

**-c, --conference**:      which conference you want to crawl（CCS\USENIX\NDSS\SP）

**-y, --year**:            which year you want to crawl

optional arguments:

**-k, --keyword**:        keywords you want papers include, default: None


# 编写时间流
- 2023.9.23 
    - 还是放弃做成一个小的命令行工具。之前是想做成一个web app的，但是因为觉得涉及到文件的存储等一系列的优化，觉得有点麻烦。
    - 实际上，在开发中试用发现不是自己想象的样子，每次调用函数都要去对论文网站爬虫，导致速度会很慢，所以，缓存变得很重要。暂时先存入文件。
    - SP的爬取还需要完善，摘要和pdf下载链接都可以有
    - CCS的爬取还有问题，不得不说CCS的网站写的很恶心
    - 晚上完善了SP的爬取，增加了摘要
- 2023.9.24
    - CCS屡屡出现问题，去点开每年的网站，发现几乎每年的accepted papers页面的链接和html排版都不一样，爬不了一点。顶级反扒技巧
