
data=read.csv("f:/volumn.csv", header=TRUE)
vma5=data$v_ma5
vma20=data$v_ma20

plot(vma5, type='o', col='blue')
abline(h=median(vma5), col='blue')
par(new=TRUE)
plot(vma20, type='o', col='red')
abline(h=median(vma20), col='red')


