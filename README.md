# Security_Papers_Crawling
## Introduction
In this repo, we realize a crawler to crawl papers in S&P/CCS/USENIX Security/NDSS for reading papers in the security field according to the given keywords.

在本仓库，我们实现了一个根据给定关键词来爬取安全四大会论文的爬虫。

## Motivation
To our best knowledge, among existing crawlers in github, none has realized crawling papers according to the keywords, which makes screening papers still time-consuming.

我没找到现有可以实现根据关键词爬取论文的爬虫，就很烦，就自己实现一个。

## Method
We use new bing to help us code.

我用new bing辅助写的爬虫

## Implement
python *_Crawling.py [-C --conference] [-Y --year] [-F --save_folder] [-K --keywords]

example: **python CCS_Crawling.py -C ccs -Y 2022 -F paper/ -K adversarial**

necessary arguments:

**-C, --conference**:      which conference you want to crawl

**-Y, --year**:            which year you want to crawl

optional arguments:

**-F, --save_floder**:     where papers downloaded, default: paper/

**-K, --keywords**:        keywords you want papers include, default: None

## Limitation
- Sensitive to Conference (This crawler may not work for another conferences)
- Keywords only support the list of single word, like [membership, adversarial] (will support like [membership inference, adversarial attack] in the future)

## Version
- 0.3 (2023.3.28) For All S&P, and papers downloaed are renamed to their titles.
- 0.2 (2023.3.15) For All CCS
- 0.1 (2023.3.15) For CCS2022 only
# Security_Papers_Crawling
