
data=read.csv("f:/volumn.csv", header=TRUE)
ma5=data$ma5
ma20=data$ma20

plot(ma5, type='o', col='blue')
par(new=TRUE)
plot(ma20, type='o', col='red')

ma5_sum=summary(ma5)
ma5_ref=as.vector(ma5_sum)
cat(ma5_ref[2], "  ", ma5_ref[3], "  ", ma5_ref[5], "\n")
abline(h=ma5_ref[2], col='blue1')
abline(h=ma5_ref[3], col='blue2')
abline(h=ma5_ref[5], col='blue3')

ma20_sum=summary(ma20)
#print(ma20_sum)
cat(ma20_sum[2], "  ", ma20_sum[3], "  ", ma20_sum[5], "\n")
ma20_ref=as.vector(ma20_sum)
abline(h=ma20_ref[2], col='red1')
abline(h=ma20_ref[3], col='red2')
abline(h=ma20_ref[5], col='red3')

