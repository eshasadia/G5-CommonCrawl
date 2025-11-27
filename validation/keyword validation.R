## validation
## save a small section to validate by hand

library(tidyverse)

validate2025 = 'problem5_govuk_filtered.csv' %>% read_csv

set.seed(123)
validate2025_train = validate2025[sample.int(352, size = 20),]

validate2025_train %>% 
  mutate(humanKeyword = '') %>%
  write_csv('validate me key words (prob5 filtered).csv')
