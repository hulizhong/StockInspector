##
# read volume data and draw pic from qfq.csv 
#     date  open  high close   low   volume     amount
#
########

data=read.csv("f:/qfq.csv", header=TRUE)

## Get data and summary it.
dvolume=data$volume
dvolumeSum=summary(dvolume)
line14=dvolumeSum[2]
line24=dvolumeSum[3]
line34=dvolumeSum[5]
print(line14)

## Get 1/4 data And summary it.
d1volume=dvolume[dvolume<=line14]
d1volumeSum=summary(d1volume)
line114 = d1volumeSum[2]
line124 = d1volumeSum[3]
line134 = d1volumeSum[5]
cat(line114, line124, line134, '\n')

## Get 2/4 data And summary it.
#d2volume=dvolume[line14<dvolume and dvolume<=line24]
#d2volumeSum=summary(d2volume)
#line214 = d2volumeSum[2]
#line224 = d2volumeSum[3]
#line234 = d2volumeSum[5]
#cat(line214, line224, line234, '\n')

## draw pic
plot(dvolume, type='o', main="view volume", xlab='<<<time<<<', ylab='volume');
abline(h=line114, col='gold1')
abline(h=line124, col='gold2')
abline(h=line134, col='gold3')
abline(h=line14, col='gold')

abline(h=line24, col='blue')
abline(h=line34, col='red')


