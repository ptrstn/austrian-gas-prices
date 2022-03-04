library(ggplot2)
library(plotly)
library(readr)

vienna_SUP <- read_csv(
  "data/vienna_SUP.csv", 
  col_types = cols(
    identifier = col_integer(), 
    timestamp = col_datetime(format = "%Y-%m-%d %H:%M"),
    postal_code = col_character()
    )
  )

austria_SUP <- read_csv(
  "data/austria_SUP.csv", 
  col_types = cols(
    identifier = col_integer(), 
    timestamp = col_datetime(format = "%Y-%m-%d %H:%M"),
    postal_code = col_character()
  )
)

View(vienna_SUP)
View(austria_SUP)

vienna_SUP %>% ggplot(aes(timestamp, price)) + geom_smooth()
austria_SUP %>% ggplot(aes(timestamp, price)) + geom_smooth()

# Make a super simple plot
p <- iris %>%
  ggplot(aes(Petal.Length, Petal.Width, color=Species)) + 
  geom_point()
p
