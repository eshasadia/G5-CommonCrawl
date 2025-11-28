# Bristol common crawl datathon repository (G5-CommonCrawl)

# Requires
- python for data wrangling and classification
- R for some data viz and some proto-type scripts (e.g. making API calls to LLMs)

## Task/ folder

- `validation`: Validation file of 20 url contents (2025). Helena and Meng Le picked out keyword independently. Also sent to copilot to check accuracy and agreement between human/llm



## data

- `news_filtered_xxxx.csv`: Filtered file from 2024/2025 crawl. Filtered to urls that contain `gov.uk/government/news`. Produced by code in `FilterURL.py` where polars is used to check url first before reading in lines.

- `policy_classes_xxx`: Contents classified but using a LLM (Gemma 3) on VM

- `\classified`: Contents classified but this time using a LLM on Groq

## test embedded graph

# My Report

Here’s the interactive chart:

<iframe src="docs/example plot.html" width="800" height="600" style="border:none;"></iframe>
