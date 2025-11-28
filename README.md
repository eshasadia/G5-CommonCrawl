# Bristol common crawl datathon repository (G5-CommonCrawl)
This repository contains the workflow, data, and analysis code produced by Group 5 for the Bristol Datathon on Common Crawl. Our project investigates policy change within the “Creating Opportunities / Breaking Down Barriers to Opportunity” mission, focusing specifically on the Best Start in Life agenda.

Using archived .gov.uk webpages from Feb–Mar 2024 and Oct 2025, we apply text processing, embedding-based semantic comparison, and clustering to identify how the discourse around early-years policy has shifted following the UK General Election (July 2024).

## Team Members
Meng Le Zhang

Aditi Dutta

Esha Sadia Nasir

Mariam Cook

Helena Byrne

E Chern Wong

# Project Overview

We analysed a large cache of UK governmental webpages extracted from the Common Crawl. Due to file size constraints, the data was accessed via cloud notebooks and filtered to isolate policy-relevant subdomains.

Our workflow included:

1. URL identification for domains associated with early-years policy.

2. Keyword-driven filtering to extract relevant text spans from large .csv datasets.

3. Embedding generation (BERT) for semantic comparison of policy language across time.

4. Clustering & PCA to visualise shifts in discourse between 2024 and 2025.

5. Press release metadata extraction (date, organisation, headline, subtopics).

6. Validation using a combination of human coders and LLM-based summarisation.


# Repository Structure
## `/data/`

Contains processed and filtered datasets.

news_filtered_*.csv
Filtered samples from both 2024 and 2025 crawls, limited to URLs containing
gov.uk/government/news.
These were generated using FilterURL.py, which uses polars to check URLs efficiently before loading content.

policy_classes_*
Text content classified using Gemma 3 on a VM for topic detection.

classified/
Classification outputs produced using Groq-hosted LLMs for comparison.

## `/validation/`

Contains validation results for 20 manually reviewed URL contents (2025).

Helena and Meng independently extracted keywords.

The same URLs were processed using Copilot to assess LLM vs human agreement.

Notes include common LLM failure modes (e.g., misinterpreting link text as body content due to WET file formatting).

## `/notebooks/` (referenced externally in Colab)

Links used during development:

Reading & parsing data:
https://colab.research.google.com/drive/1Y8OIDSFNeWqP1hBvSiCvSt0-ozkKrd8J?usp=sharing

Generating embeddings:
https://colab.research.google.com/drive/1MSg-4xyR1RRjLLxVMFJxvWXHUjMAWIOI?usp=sharing


These notebooks contain:

Data loading and preprocessing scripts

Keyword-based sampling of text windows

Embedding generation and similarity matrices

PCA and clustering visualisation code




# Requirements
`Python`: Data wrangling (Polars, Pandas), Keyword extraction, Embedding generation, Clustering and semantic analysis

`R`: Data visualisation prototypes, Scripts for calling external LLM APIs





# Analysis Summary

Core policy terms included:

['Best Start in Life', 'Sure Start', 'family hubs', 'free school meals', 
 'School meals', 'Development checks', 'School readiness', 'breakfast clubs',
 'free breakfast', 'childcare hours', 'free childcare hours',
 'free childcare for working parents', 'tax-free childcare',
 'universal credit childcare']


We compared 2024 vs 2025 text embeddings to explore:

- Policy topics that persisted across governments

- Emerging or discontinued discourse

- Semantic drift (e.g., Best Start in Life and family hubs becoming nearly identical in 2025, suggesting policy repositioning)

Outputs include:

- Cosine similarity matrices

- PCA embeddings

- Cluster maps

- Summary tables of policy mentions

A comparison spreadsheet is available here:
https://docs.google.com/spreadsheets/d/13n3gUIBtA1DpU14Wpvb-2o08nLG0drN4iTlRpzgIKEQ/edit?usp=sharing




## Visualisation Example

Interactive PCA & cluster plots are included in /docs.

Example:

<iframe src="docs/example plot.html" width="800" height="600" style="border:none;"></iframe>



## Notes on Validation & Limitations

The WET files contain plain text only, causing LLMs to misinterpret navigation links as body content.

Human validation showed good accuracy overall, but LLMs sometimes hallucinated or over-interpreted hyperlinks.

Some ministerial subdomains lacked coverage in specific crawls (0 occurrences).


## Future Work

Extend analysis to additional subdomains (e.g., /organisations/)

Improve causal relation extraction between policy mentions

Apply topic modelling or supervised classifiers on a larger corpus

Construct a time-series narrative of policy shifts post-2024 election



