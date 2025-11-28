# script to scrape html elements from active website
## used to get heading removed from WET files
## author: E Chern Wong 

import time
import random
import requests
from bs4 import BeautifulSoup
import polars as pl

# ---------------------------------------------------------
# Helper function to find GOV.UK metadata (From, Published)
# ---------------------------------------------------------
def _get_metadata_value(soup, term_text):
    dts = soup.find_all("dt", class_="gem-c-metadata__term")
    for dt in dts:
        if dt.get_text(strip=True).lower().startswith(term_text.lower()):
            dd = dt.find_next_sibling("dd", class_="gem-c-metadata__definition")
            if dd:
                return dd
    return None

# ---------------------------------------------------------
# Function: Scrape a single GOV.UK page
# ---------------------------------------------------------
def scrape_govuk(url):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Category
        cat_el = (
            soup.select_one("span.gem-c-heading__context")
            or soup.select_one("span.govuk-caption-xl")
            or soup.select_one(".govuk-caption-s")
        )
        category = cat_el.get_text(strip=True) if cat_el else None

        # Title
        title_el = soup.select_one("h1.govuk-heading-l") or soup.select_one("h1")
        title = title_el.get_text(strip=True) if title_el else None

        # Subtitle / lead
        subtitle_el = (
            soup.select_one("p.gem-c-lead-paragraph")
            or soup.select_one("div.gem-c-title__context")
        )
        subtitle = subtitle_el.get_text(strip=True) if subtitle_el else None

        # From
        from_dd = _get_metadata_value(soup, "From")
        if from_dd:
            parts = []
            for node in from_dd.contents:
                if getattr(node, "name", None) == "a":
                    parts.append(node.get_text(strip=True))
                else:
                    text = getattr(node, "string", None)
                    if text:
                        t = text.strip()
                        if t:
                            parts.append(t)
            from_text = " ".join(p for p in parts if p).replace(" ,", ",")
        else:
            from_text = None

        # Published date
        published_dd = _get_metadata_value(soup, "Published")
        if published_dd:
            t = published_dd.find("time")
            published = t.get_text(strip=True) if t else published_dd.get_text(strip=True)
        else:
            t = soup.select_one("time[datetime]")
            published = t.get_text(strip=True) if t else None

        # Body text
        body_paras = [p.get_text(strip=True) for p in soup.select("div.gem-c-govspeak p")]
        if not body_paras:
            body_paras = [
                p.get_text(strip=True)
                for p in soup.select("article p, article .govuk-body, article .govuk-body-l")
            ]
        body = "\n\n".join(body_paras)

        return {
            "url": url,
            "category": category,
            "title": title,
            "subtitle": subtitle,
            "from": from_text,
            "published": published,
            "content": body,
        }

    except Exception as e:
        return {
            "url": url,
            "category": None,
            "title": None,
            "subtitle": None,
            "from": None,
            "published": None,
            "content": None,
            "error": str(e),
        }

# ---------------------------------------------------------
# Step 1: Load list of URLs
# ---------------------------------------------------------
df = pl.read_csv("news_filtered_2024_p1_2.csv")
urls = df["url"].to_list()

print(f"Loaded {len(urls)} URLs.")

# ---------------------------------------------------------
# Step 2: Scrape all URLs (with polite delay)
# ---------------------------------------------------------
results = []
for i, url in enumerate(urls, 1):
    print(f"[{i}/{len(urls)}] Scraping: {url}")
    data = scrape_govuk(url)
    results.append(data)

    # polite delay to avoid rate limiting
    time.sleep(random.uniform(1.2, 2.5))

# ---------------------------------------------------------
# Step 3: Save output CSV
# ---------------------------------------------------------
out = pl.DataFrame(results)

out.write_csv("2024p1_2_scraped_output.csv")

print("\n🎉 DONE! Saved govuk_scraped_output.csv")
