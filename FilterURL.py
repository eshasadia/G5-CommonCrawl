

import polars as pl

# Lazy loading: memory safe
df = (
    pl.scan_csv("problem4_govuk_split2.csv")
    .filter(pl.col("url").str.contains("www.gov.uk/government/organisations"))
    .collect()
)

# Save result
df.write_csv("filtered_2024_p2.csv")

print("Done! Filtered rows:", df.shape)
