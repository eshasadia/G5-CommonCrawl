# Bristol CommonCrawl Datathon

# Problem Statement
This is a cache of web data, which contains all the UK governmental webpages (.gov.uk) that have been archived by the Common Crawl in two points in time: February-March 2024 (part 1 and part 2 same as Problem 4) and October 2025. Identify changes in a specific policy domain associated with the new government elected in July 2024.

# Team
We are a group of data scientists at a datathon using commoncrawl data to solve a problem



This repository contains all our code.

# Methods
To tackle the problem, we first:
- Targeted our searched. We had 2.4 million website entries in the raw WET file. To look at policies, we explicitly filtered our data to website in the `gov.uk/government/news` subdomain. This is where new policies are announced. This gives us roughly to 3000 webpages. 


To analyse the webiste content, we took two approach:
- Target approached. We had a 'seed' of 12 policy names or terms. We filtered our data to only webpages that mentioned these terms. Then we generated embeddings to look at differences in context for the same terms across time.
- LLM approach to read documents and classify any policy instruments into certain categories. Then we compared differences in classifications over time. 

# Results


# Classifications:


## Task/ folder

`validation`: Validation file of 20 url contents (2025). Helena and Meng Le picked out keyword independently. Also sent to copilot to check accuracy and agreement between human/llm

## data

`news_filtered_xxxx.csv`: Filtered file from 2024/2025 crawl. Filtered to urls that contain `gov.uk/government/news`. Produced by code in `FilterURL.py` where polars is used to check url first before reading in lines.


## test embedded graph

# My Report

Here’s the interactive chart:

<iframe src="docs/example plot.html" width="800" height="600" style="border:none;"></iframe>
