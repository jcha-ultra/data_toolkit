# minimal example of a neural net
library("neuralnet")
training_data <- read.csv("~/repos/toolkit/datasets/roots.csv", header = TRUE)
model <- neuralnet(formula = root_k ~ k, data = training_data, hidden = 10)
output <- cbind(training_data, nn_output = unlist(model$net.result))