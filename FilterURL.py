import polars as pl
import os

# Input CSV files
input_files = [
    "problem4_govuk_split1.csv",
    "problem4_govuk_split2.csv",
    "problem5_govuk.csv"
]

# Filter string
url_filter = "government/news"

# Loop over files
for file in input_files:
    print(f"Processing {file}...")
    
    # Lazy load, filter, and collect
    df = (
        pl.scan_csv(file)
          .filter(pl.col("url").str.contains(url_filter))
          .collect()
    )
    
    # Generate output file name
    base_name = os.path.splitext(file)[0]  # removes .csv
    output_file = f"{base_name}_filtered.csv"
    
    # Save filtered CSV
    df.write_csv(output_file)
    
    print(f"Done! Filtered rows: {df.shape}, saved to {output_file}\n")










