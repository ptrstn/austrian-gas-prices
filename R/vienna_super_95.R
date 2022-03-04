library(ggplot2)
library(plotly)
library(readr)
library(dplyr)


austria_SUP <- read_csv(
  "data/austria_SUP.csv", 
  col_types = cols(
    station_id = col_integer(), 
    timestamp = col_datetime(format = "%Y-%m-%d %H:%M")
  )
)

austria_DIE <- read_csv(
  "data/austria_DIE.csv", 
  col_types = cols(
    station_id = col_integer(), 
    timestamp = col_datetime(format = "%Y-%m-%d %H:%M")
  )
)

austria_GAS<- read_csv(
  "data/austria_GAS.csv", 
  col_types = cols(
    station_id = col_integer(), 
    timestamp = col_datetime(format = "%Y-%m-%d %H:%M")
  )
)

vienna_SUP <- read_csv(
  "data/vienna_SUP.csv", 
  col_types = cols(
    station_id = col_integer(), 
    timestamp = col_datetime(format = "%Y-%m-%d %H:%M")
    )
  )

vienna_DIE <- read_csv(
  "data/vienna_DIE.csv", 
  col_types = cols(
    station_id = col_integer(), 
    timestamp = col_datetime(format = "%Y-%m-%d %H:%M")
  )
)

vienna_GAS<- read_csv(
  "data/vienna_GAS.csv", 
  col_types = cols(
    station_id = col_integer(), 
    timestamp = col_datetime(format = "%Y-%m-%d %H:%M")
  )
)

gas_stations <- read_csv(
  "data/gas_stations.csv",
  col_types = cols(
    station_id = col_integer(), 
    postal_code = col_character()
    )
  )

vienna <- bind_rows(vienna_SUP, vienna_DIE, vienna_GAS)
austria <- bind_rows(austria_SUP, austria_DIE, austria_GAS)

data <- austria %>% left_join(gas_stations)

View(austria)
View(data)

data %>% ggplot(aes(timestamp, price, color = label)) + geom_smooth()

                