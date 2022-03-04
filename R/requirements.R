# Try to load package manager "pacman" and install it if loading failed
if (!require("pacman")) install.packages("pacman")
library("pacman")

# use pacman::p_load to effectively install and load packages
p_load("here")
p_load("ggplot2")
p_load("readr")
p_load("plotly")
