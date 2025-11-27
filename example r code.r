# raw_text = the dataframe with content for url

# Step 1: Basic cleanup


clean_text <- 
  raw_text %>%
  mutate(
    content = content %>% str_replace_all("\n", " ") %>%              # replace newlines with spaces
    str_replace_all("<.*?>", " ") %>%           # remove HTML tags if present
    str_replace_all("\\s+", " ") %>%            # collapse multiple spaces
    str_trim()                                  # trim leading/trailing spaces
  )

# Step 2: Remove boilerplate patterns

## load in boiler plate patterns
source('boilerplate patterns.r')
clean_text
  
clean_text = 
  clean_text %>%
  mutate(content = str_remove_all(content, regex(paste(boilerplate_patterns, collapse="|"), ignore_case = TRUE))) %>%
  mutate(content = str_squish(content))   # normalize whitespace


# Step 3: Normalize punctuation and spacing
clean_text <- 
  clean_text %>%
  mutate(content =
           content %>%
  str_replace_all("0items", "0 items") %>%
  str_replace_all("…", "") %>%
  str_replace_all("\\s+", " ")
  )


# Step 4: save the file 
clean_text %>% write_csv('crawl 2024 (init clean).csv')



