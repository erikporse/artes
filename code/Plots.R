setwd("~/Documents/Research/Ecology_Energy_Climate/Water Resources/Countries and Regions/California/Southern California/Systems Analysis/Artes Model/Calibration/Step 4")

actual <- read.csv2(file="Actual Calib Nodes.csv",head=TRUE,sep=",")
modeled <- read.csv2(file="Modeled Calib Nodes.csv",head=TRUE,sep=",")

actual2 <- t(actual)
modeled2 <- t(modeled)

actual_noheads <- actual2[-1,]
modeled_noheads <- modeled2[-1,]

#months <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec")
months = labels(actual_noheads[,1])
years <- seq(1986,2010,2)

a<-ts(actual_noheads,start=c(1986,1),freq=12)
b<-ts(modeled_noheads,start=c(1986,1),freq=12)

for (reach in 1:length(actual2[1,])){
  minY = min(0, 0)
  maxY = (max(max(as.numeric(actual_noheads[,reach]),as.numeric(modeled_noheads[,reach]))))
  
  plot(a[,reach],xlab="Time",ylab="Flows (ac-ft)",main=as.character(actual2[1,][reach]),
       type="o",col="blue",xlim=c(1986,2010),ylim=c(0,maxY),axes=F)    
  lines(b[,reach],col="red")
  axis(1,at=years,labels=years,las=2);axis(2);box()
}
