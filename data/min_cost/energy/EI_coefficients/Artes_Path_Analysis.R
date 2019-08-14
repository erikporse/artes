########################################################
#
# An algorithm to identify paths in water resource supply, 
# distribution, and treatment network
#
# Created by Erik Porse
# April 26, 2019
#
########################################################

## Read in Data
setwd("C:/Mac Files/Documents/Research/Ecology_Energy_Climate/Water Resources/Countries and Regions/California/Southern California/Systems Analysis/Networks/Paths/")

nodes <- read.csv("Artes_Nodes.csv", header=T, as.is=T)
links <- read.csv("Artes_Links.csv", header=T, as.is=T)
source_nodes <- read.csv("Artes_Sources.csv", header=T, as.is=T)

head(nodes)

head(links)

nrow(nodes); length(unique(nodes$id))

nrow(links); nrow(unique(links[,c("from", "to")]))

## Turn data into igraph objects
library(igraph)

net <- graph_from_data_frame(d=links, vertices=nodes, directed=T) 
E(net)$weight <- links$total_ei

dist.from <- distances(net, v=V(net)[nodes==source_nodes$id[1]], to=V(net))

for (i in 2:nrow(source_nodes)) {
    dist.from <- rbind(dist.from,distances(net, v=V(net)[nodes==source_nodes$id[i]], to=V(net)))
}

write.csv(dist.from,"ei_by_link.csv")
