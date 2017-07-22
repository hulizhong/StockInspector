
data=read.csv("f:/volumn.csv", header=TRUE)
vma5=data$v_ma5
vma20=data$v_ma20

plot(vma5, type='o', col='blue')
par(new=TRUE)
plot(vma20, type='o', col='red')


vma5_sum=summary(vma5)
vma5_ref=as.vector(vma5_sum)
cat(vma5_ref[2], "  ", vma5_ref[3], "  ", vma5_ref[5], "\n")
abline(h=vma5_ref[2], col='blue1')
abline(h=vma5_ref[3], col='blue2')
abline(h=vma5_ref[5], col='blue3')

vma20_sum=summary(vma20)
vma20_ref=as.vector(vma20_sum)
cat(vma20_ref[2], "  ", vma20_ref[3], "  ", vma20_ref[5], "\n")
abline(h=vma20_ref[2], col='red1')
abline(h=vma20_ref[3], col='red2')
abline(h=vma20_ref[5], col='red3')

