## plots of data to save 
library(dplyr)
library(plotly)

n_sample = 100
?sample
df = 
  data.frame(
    policy.instrument = 1:100,
    main.classification = letters[1:4] %>% sample(size = n_sample, replace = T),
    secondary.classification = letters[1:4] %>% sample(size = n_sample, replace = T),
    time = 2024:2025 %>% as.character
  )
df

library(ggplot2)
library(plotly)
library(htmlwidgets)

gg_version = 
  ggplot(df, aes(y = main.classification, fill = time, group = time)) +
  geom_bar(position = position_dodge())


## save by hand
gg_version %>% ggplotly() %>% htmlwidgets::saveWidget('docs/example plot.html')
?ggplotly
