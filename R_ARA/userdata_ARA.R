# userdata Association Rule Analysis
# userdata(ID, Gamename)

# set working directory
setwd("D:/Project/test")

# association rule analysis package
library(arules)

# data import-> make transaction data
udata1<-read.csv("merge_new_userdata_notime.csv")
head(udata1)

udata.list<-split(udata1$Game,udata1$ID)

udata.trans<-as(udata.list,"transactions")
# warning(s) : In asMethod(object) : removing duplicated items in transactions

udata.trans

# summary of userdata
summary(udata.trans)
#density : 0.016, 373*1104 cell -> 1.6%

# for running dvdtras data
# apriori(transaction, parameter=list(support=list(support=0.0#, confidence=0.##))
udata_rule<-apriori(udata.trans,parameter = list(support=0.2,confidence = 0.20,minlen = 2))
 
udata_rule
# 19 rules

inspect(udata_rule)

summary(udata_rule)

# Bar chart for support>0.2
itemFrequencyPlot(udata.trans,support=0.2,main="item for support>=0.2", col="blue")

