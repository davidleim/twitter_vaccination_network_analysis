library(igraph)
library("leiden")
library(tidyverse)

# Load graph exports from python iGraph
files = list.files( pattern="*.graphml")
graphlist <- list()

for (graph in files){
  g <- read_graph(graph, format = "graphml")
  name <- paste('item:',graph,sep='')
  graphlist[[name]] <- g
}

# Density measure
percent_density <- function(x) {
  (ecount(x)/((vcount(x)*(vcount(x)-1)/2)))*100
}

network_statistics <- function(x) {
  print(names(x))
  print('Node count')
  print(vcount(x))
  print('Edge count')
  print(ecount(x))
  density <- percent_density(x)
  centralization <- centr_degree(x,
                                 mode = "all",
                                 loops = FALSE, 
                                 normalized = TRUE)$centralization
  print('normalized centralization =')
  print(centralization)
  print('density =')
  print(density)
  print('assortativity degree =')
  print(assortativity_degree(x, directed = FALSE))
  
}

i = 0
for (g in graphlist) {
  i = i+ 1
  print(names(graphlist)[i])
  network_statistics(g)
  print('___________________________________')
}


