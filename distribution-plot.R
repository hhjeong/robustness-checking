
par(mfrow = c(3,3))
profile <- c( "mRNA", "CNA", "METH" )
measure <- c( "cor", "mi", "mina" )


pdf("density.pdf")
par(mfrow = c(3,3))
for( p in profile ) {
  for( m in measure ) {
    case <- read.table(sprintf('result/%s/%s_filtered.txt', m,p))
    
    pf <- ""
    if(m=="cor") pf <- p
    
    boundx <- c(0,1)
    if( m == "mina" ) boundx <- c(0,0.2)
    else if( m == "cor" ) boundx <- c(0,2)
    
    plot(log10(case$V2)~case$V1,  xlim=boundx, ylim=c(0,6),type='n',xlab="",ylab=pf,main=m)
    
    
    for(i in 0:99) {
      case <- read.table(sprintf('result/%s/%s_filtered_random%d.txt',m,p,i))
      points(log10(case$V2)~case$V1,type='l',lwd=0.5,col='gray')
    }
    case <- read.table(sprintf('result/%s/%s_filtered.txt', m,p))
    points(log10(case$V2)~case$V1, ylim=c(0,6),type='l',col="#CC0000",lwd=2,xlab="",ylab="")
    
  }
}

dev.off()

pdf("cumulative.pdf")
par(mfrow = c(3,3))

for( p in profile ) {
  for( m in measure ) {
    case <- read.table(sprintf('result/%s/%s_filtered.txt', m,p))
    
    pf <- ""
    if(m=="cor") pf <- p
    
    boundx <- c(0,1)
    if( m == "mina" ) boundx <- c(0,0.2)
    else if( m == "cor" ) boundx <- c(0,2)
    plot(log10(sum(case$V2)-cumsum(case$V2))~case$V1, xlim=boundx,type='n',xlab="",ylab=pf,main=m)
    
    
    for(i in 0:99) {
      case <- read.table(sprintf('result/%s/%s_filtered_random%d.txt',m,p,i))
      points(log10(sum(case$V2)-cumsum(case$V2))~case$V1,type='l',lwd=0.5,col='gray')
    }
    case <- read.table(sprintf('result/%s/%s_filtered.txt', m,p))
    points(log10(sum(case$V2)-cumsum(case$V2))~case$V1, ylim=c(0,6),type='l',col="#CC0000",lwd=2,xlab="",ylab="")
    
  }
}
dev.off()
