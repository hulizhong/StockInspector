
data=read.csv("f:/volumn.csv", header=TRUE)
p=data$open

p_sum=summary(p)
p_ref=as.vector(p_sum)
cat(p_sum[2], "  ", p_sum[3], "  ", p_sum[5], "\n")

plot(p, type='o', col='blue')
abline(h=p_ref[2], col='blue1')
abline(h=p_ref[3], col='blue2')
abline(h=p_ref[5], col='blue3')

