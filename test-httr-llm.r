## LLM
library(tidyverse)
library(httr)
library(jsonlite)

## readi in the filtered file 

news_df = 'data/news_filtered_2025.csv' %>% read_csv
# Set your Groq API key as an environment variable first:
# Sys.setenv(GROQ_API_KEY = "your_api_key_here")

url <- "https://api.groq.com/openai/v1/chat/completions"

headers <- add_headers(
  Authorization = paste("Bearer", groq_api),
  "Content-Type" = "application/json"
)

prompt_classifiy <- 
"You will be given a government news item.

Instructions:
1. Identify any explicit or implicit policy instruments mentioned in the text.
2. For each instrument, classify it into one of the following main categories:
   - Welfare (e.g., grants, benefits, subsidies)
   - Monetary (e.g., tax changes, fiscal incentives)
   - Legislative (e.g., new laws, regulations, statutory changes)
   - Administrative (e.g., new guidelines, standards, reporting requirements)
   - Institutional (e.g., creation of new agencies)
   - Market-based (e.g., trading permits, carbon pricing)
   - Informational (e.g., public awareness campaigns, nudging)
   - Other (e.g., strategic plans, consultations)
3. If relevant, add a secondary classification (e.g., both welfare and legislative).
4. Output ONLY a json with the following keys:
   - Policy.Instrument
   - Main.Classification
   - Secondary.Classification
   - Orig.url
5. Do not include any explanation, commentary, or text outside the table.
6. Add the orig.url in orig.url

This is the content to inspect:"


## pick a line
this_line = 3

body <- toJSON(list(
  model = "llama-3.1-8b-instant",   # Example Groq model
  messages = list(
    list(role = "system", content = "You are a helpful assistant."),
    list(role = "user", content = 
    prompt_classifiy %>% 
      paste(news_df$content[this_line]) %>%
      paste("orig.url =", news_df$url[this_line])
    
    )

  )
), auto_unbox = TRUE)

res <- POST(url, headers, body = body)

# Parse response
parsed <- content(res, as = "parsed", type = "application/json")
cat(parsed$choices[[1]]$message$content)
cat(parsed$choices[[1]]$message$content, file = 'test.json') 
parsed$choices[[1]]$message$content

messy_string = cat(parsed$choices[[1]]$message$content) %>% capture.output()



## Groq uses a common open ai structure:
# 
# {
#   "model": "llama-3.1-70b-versatile",
#   "messages": [
#     { "role": "system", "content": "You are a helpful assistant." },
#     { "role": "user", "content": "Explain the difference between Version 1 and Version 2 of this text." }
#   ],
#   "temperature": 0.7,
#   "max_tokens": 512
# }


## We have to loop the table

# 4k per request tokens 
14/4
