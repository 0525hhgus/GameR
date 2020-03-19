#

setwd("D:/Project/R_userdata")  

# Userdata (ID, Game+a)
udata1 <- read.csv("userdata1.csv")

# association rule analysis
library(arules)

head(udata1)
