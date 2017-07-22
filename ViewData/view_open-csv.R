
data=read.csv("f:/volumn.csv", header=TRUE)
p=data$open

plot(p, type='o', col='blue')
abline(h=median(p), col='blue')

