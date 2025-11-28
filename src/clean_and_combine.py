import pandas as pd

d1 = pd.read_csv('govuk_articles.csv')
d1.isnull().sum()
d1 = d1.dropna()

d2 = pd.read_csv('Scraped_2024_p2.csv')
d2.isnull().sum()
d2 = d2.dropna()

d3 = pd.read_csv('Scraped_2025.csv')
d3.isnull().sum()
d3 = d3.dropna()

d1 = d1.rename(columns={
    'article_type': 'category',
    'published_date': 'published',
    'ministry': 'from',
    'description': 'subtitle'
})

d1 = d1.drop(columns={'schema_name'})

d24 = pd.concat([d1, d2])

d24.to_csv('../data/clean_scrape_data_2024.csv')
d3.to_csv('../data/clean_scrape_data_2025.csv')
