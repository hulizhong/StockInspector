
data=read.csv("f:/volumn.csv", header=TRUE)
ma5=data$ma5
ma20=data$ma20

plot(ma5, type='o', col='blue')
abline(h=median(ma5), col='blue')
par(new=TRUE)
plot(ma20, type='o', col='red')
abline(h=median(ma20), col='red')


