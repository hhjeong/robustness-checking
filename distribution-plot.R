
dev.off()
par(mfrow = c(3,3))
profile <- c( "mRNA", "CNA", "METH" )
measure <- c( "cor", "mi", "mina" )

for( p in profile ) {
  for( m in measure ) {
    case <- read.table(sprintf('result/%s/%s_filtered.txt', m,p))
    # plot(log10(sum(case$V2)-cumsum(case$V2))~case$V1, ylim=c(0,6),type='n',xlab="",ylab="")
    plot(log10(case$V2)~case$V1, ylim=c(0,6),type='n',xlab="",ylab="")
    
    
    for(i in 0:99) {
      case <- read.table(sprintf('result/%s/%s_filtered_random%d.txt',m,p,i))
      #points(log10(sum(case$V2)-cumsum(case$V2))~case$V1,type='l',lwd=0.5,col='gray')
      points(log10(case$V2)~case$V1,type='l',lwd=0.5,col='gray')
    }
    case <- read.table(sprintf('result/%s/%s_filtered.txt', m,p))
    #points(log10(sum(case$V2)-cumsum(case$V2))~case$V1, ylim=c(0,6),type='l',col="red",lwd=4,xlab="",ylab="")
    points(log10(case$V2)~case$V1, ylim=c(0,6),type='l',col="red",lwd=4,xlab="",ylab="")
    
  }
}
