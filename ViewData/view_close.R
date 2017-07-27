##
# read close data and draw pic from qfq.csv 
#     date  open  high close   low   volume     amount
#
########

data=read.csv("f:/qfq.csv", header=TRUE)

## Get data and summary it.
dclose=data$close
dcloseSum=summary(dclose)
line14=dcloseSum[2]
line24=dcloseSum[3]
line34=dcloseSum[5]
print(line14)

## Get 1/4 data And summary it.
d1close=dclose[dclose<=line14]
d1closeSum=summary(d1close)
line114 = d1closeSum[2]
line124 = d1closeSum[3]
line134 = d1closeSum[5]
cat(line114, line124, line134, '\n')

## draw pic
plot(dclose, type='o', main="view close", xlab='<<<time<<<', ylab='close');
abline(h=line114, col='gold1')
abline(h=line124, col='gold2')
abline(h=line134, col='gold3')
abline(h=line14, col='gold')

abline(h=line24, col='blue')
abline(h=line34, col='red')
