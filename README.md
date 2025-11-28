# Bristol CommonCrawl Datathon Repository

## Problem Statement
This is a cache of web data, which contains all the UK governmental webpages (.gov.uk) that have been archived by the Common Crawl in two points in time: February-March 2024 (part 1 and part 2 same as Problem 4) and October 2025. Identifying changes in a specific policy domain associated with the new government elected in July 2024.

## Team
Meng Le Zhang, Aditi Dutta, Esha Sadia Nasir, Mariam Cook, Helena Byrne, E Chern Wong.


## Requires
- Python for data wrangling and classification.
- R for some data visualisation and some proto-type scripts (e.g. making API calls to LLMs).

## Task/ folder

- `validation`: Validation file of 20 url contents (2025). Helena and Meng Le picked out keyword independently. Also sent to copilot to check accuracy and agreement between human/LLM.



## Data

- `news_filtered_xxxx.csv`: Filtered file from 2024/2025 crawl. Filtered to urls that contain `gov.uk/government/news`. Produced by code in `FilterURL.py` where polars is used to check url first before reading in lines.

- `policy_classes_xxx`: Contents classified but using a LLM (Gemma 3) on VM.

- `\classified`: Contents classified but this time using a LLM on Groq (llama3.1) on colab.

## Test embedded graph

## My Report

Here’s the interactive chart:

<iframe src="docs/example plot.html" width="800" height="600" style="border:none;"></iframe>
