## plots of data to save 
library(tidyverse)
library(plotly)
library(htmlwidgets)



policies_2024_df = 
  'data/policy_classes_2024.csv' %>% 
  read_csv() 

policies_2025_df = 
  'data/policy_classes_2025.csv' %>% 
  read_csv() 

## strip the published

policies_2025_df = 
  policies_2025_df %>%
  rename(
    published_2025_val = published
  )

policies_2024_df$published
policies_2025_df$published %>% as_date()

## 
all_policies_df = bind_rows(policies_2024_df, policies_2025_df)

all_policies_df =
  all_policies_df %>%
  mutate(
    `Main Classification` = 
      `Main Classification` %>% 
      gsub(x=. , 'Financial \\(Monetary\\)', 'Monetary') %>%
      gsub(x=. , 'Other \\(strategic plans\\)', 'Other') %>%
      gsub(x=. , 'Other \\(strategic plans, consultations\\)', 'Other') %>%
      gsub(x=. , 'Welfare \\(grants, benefits, subsidies\\)', 'Welfare') %>%
      gsub(x=. , 'Financial \\(grant\\)', 'Monetary') %>%
      gsub(x=. , 'Financial', 'Monetary') %>%
      gsub(x=. , 'Incentivizes', 'Other') 
      
  )


## clear/ replace

all_policies_df$`Main Classification` %>% table
all_policies_df %>% summary
policies_2025_df$published_2025_val %>% str_sub(-4, - 1) 

all_policies_df =
  all_policies_df %>%
  mutate(
    published_date = published%>% as_date(),
    published_year = published_date %>% year()
  ) %>%
  mutate(
    published_val_2025_year = published_2025_val %>% 
      str_sub(-4, - 1) %>% as.numeric(),
    published_year = ifelse(published_year %>% is.na,  published_val_2025_year, published_year)
  ) 

all_policies_df %>% summary

all_policies_df =
  all_policies_df %>% 
  mutate(
    before2025 = published_year < 2025
  )

gg_version = 
  ggplot(all_policies_df %>% filter(published_year %in% 2024:2025),
         aes(y = `Main Classification`, fill = before2025, group = before2025)
         )+
  geom_bar(position = position_dodge()) +
  ggtitle('Policy instruments 2024 vs 2025',
          subtitle = 'Content from www.gov.uk/government/news') +
  theme(legend.position = 'bottom')

gg_version
## save by hand
gg_version %>% ggplotly() # %>% saveWidget('docs/example plot.html')
#gg_version %>% ggplotly() %>% htmlwidgets::saveWidget('docs/example plot.html')
?ggplotly


gg_line_df = 
  all_policies_df %>%
  group_by(published_year, `Main Classification`) %>%
  summarise(n = n())

gg_line = 
  ggplot(gg_line_df %>% filter(published_year > 2015),
         aes(x = published_year, y = n, colour = `Main Classification`)) +
  geom_point() +
  geom_line() +
  ggtitle('Type of policies over time (post-2015)',
          subtitle = 'Content from www.gov.uk/government/news') +
  theme(legend.position = 'bottom') +
  ylab('N. policies') +
  xlab('Policy publication year')

gg_line %>% ggplotly
