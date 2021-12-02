# minimal example of a neural net
library("neuralnet")
training_data = read.csv("~/repos/toolkit/datasets/roots.csv", header=TRUE)
nn_model <- neuralnet(formula = root_k ~ k, data = training_data, hidden = 10, threshold = 0.01)
output <- cbind(training_data, nn_output = unlist(nn_model$net.result))