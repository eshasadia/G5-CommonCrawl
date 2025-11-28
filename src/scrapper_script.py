import pandas as pd
import numpy as np
import regex as re
import polars as pl
import csv
import requests
from bs4 import BeautifulSoup
import json
import time
import random

def clean_govuk_content(text):
    if pd.isna(text):
        return ""

    # 1. remove escaped newline sequences
    text = text.replace("\\n", "\n")
    text = text.replace("\n", " ")

    # 2. drop leading/trailing quotes  
    text = text.strip('\"\' ')
    

    # 3. remove cookie & banner boilerplate
    cookie_patterns = [
        r"cookies on gov\.uk.*?hide this message",
        r"We use some essential cookies.*?improve government services\.",
        r"You have accepted additional cookies.*?change your cookie settings at any time\.",
        r"You have rejected additional cookies.*?change your cookie settings at any time\.",
        r"Accept additional cookies",
        r"Reject additional cookies",
    ]
    for p in cookie_patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE | re.DOTALL)

    # 4. remove navigation menu and GOV.UK navigation items
    nav_patterns = [
        r"skip to main content",
        r"navigation menu",
        r"menu",
        r"services and information.*?government activity",
        r"support links.*", 
        r"popular on gov\.uk.*?home",
        r"services and information",
        r"government activity",
        r"departments.*?news",
        r"gov\.uk",               # remove 'gov.uk'
        r"search gov\.uk\s*×?",   # remove 'search gov.uk ×' or without ×
        r"search gov\.uk",        # remove 'search gov.uk'
        r"news stories",          # remove 'news stories'
    ]
    for p in nav_patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE | re.DOTALL)

    # 5. remove footer + licence boilerplate
    footer_patterns = [
        r"all content is available.*?$",
        r"© crown copyright.*?$",
        r"help us improve gov\.uk.*?$",
        r"privacy.*?$",
        r"terms and conditions.*?$",
        r"accessibility statement.*?$",
        r"contact.*?$",
    ]
    for p in footer_patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE | re.DOTALL)

    # 6. remove share links/social media
    text = re.sub(r"share this page.*?published", "published", 
                  text, flags=re.IGNORECASE | re.DOTALL)

    # 7. remove repeated sections ("services and information", etc.)
    text = re.sub(r"(services and information.*?)+", "", text, flags=re.DOTALL)

    # 8. remove survey/email request sections
    text = re.sub(r"help us improve gov\.uk.*?email address", "", 
                  text, flags=re.IGNORECASE | re.DOTALL)

    # 9. collapse multiple blank lines
    text = re.sub(r"\n\s*\n\s*", "\n\n", text)

    # 10. strip spaces
    text = text.strip()

    return text




def scrape_govuk_article(url):
    """Scrape a single GOV.UK news article into structured data."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"ERROR: Failed to fetch {url}: {e}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    data = {"url": url}  # keep URL for reference

    # Meta tags mapping
    meta_mappings = {
        "og:title": "title",
        "og:description": "description",
        "govuk:primary-publishing-organisation": "ministry",
        "govuk:schema-name": "schema_name",
        "govuk:public-updated-at": "published_date",
        "govuk:format": "article_type"
    }

    for meta_tag in soup.find_all("meta"):
        prop = meta_tag.get("property") or meta_tag.get("name")
        if prop in meta_mappings:
            data[meta_mappings[prop]] = meta_tag.get("content")

    # JSON-LD extraction
    json_ld_tag = soup.find("script", type="application/ld+json")
    if json_ld_tag:
        try:
            json_ld = json.loads(json_ld_tag.string)
            body_html = json_ld.get("articleBody", "")
            body_text = BeautifulSoup(body_html, "html.parser").get_text(separator="\n")
            data["content"] = body_text

            data.setdefault("title", json_ld.get("name"))
            data.setdefault("description", json_ld.get("description"))
            data.setdefault("published_date", json_ld.get("datePublished"))
            data.setdefault("article_type", json_ld.get("@type"))

        except json.JSONDecodeError as e:
            print(f"ERROR: JSON-LD parsing failed for {url}: {e}")

    return data

def scrape_govuk_dataset(url_list, output_csv="govuk_articles.csv", min_wait=2, max_wait=4):
    """Scrape multiple GOV.UK URLs and store DataFrame incrementally."""
    all_articles = []

    # Load existing CSV if present
    if os.path.exists(output_csv):
        df_existing = pd.read_csv(output_csv)
        scraped_urls = set(df_existing["url"].tolist())
        all_articles = df_existing.to_dict("records")
        print(f"Resuming. {len(scraped_urls)} articles already scraped.")
    else:
        scraped_urls = set()

    for i, url in enumerate(url_list, 1):
        if url in scraped_urls:
            print(f"Skipping already scraped URL: {url}")
            continue

        print(f"Scraping {i}/{len(url_list)}: {url}")
        article = scrape_govuk_article(url)
        if article:
            all_articles.append(article)
            # Save after each instance
            df_temp = pd.DataFrame(all_articles)
            df_temp.to_csv(output_csv, index=False)
            print(f"Saved {len(all_articles)} articles to {output_csv}")
        else:
            print(f"WARNING: No data returned for {url}")
            continue

        # Random wait
        wait_time = random.uniform(min_wait, max_wait)
        print(f"Waiting {wait_time:.1f} seconds...")
        time.sleep(wait_time)

    return pd.DataFrame(all_articles)


