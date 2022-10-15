library(caret)

# demo function for minimally functional classification example: predicts the Species of a flower in the `iris` dataset based on the other columns
run_classification_example <- function() {
  # create training/testing partition
  set.seed(1)
  training_idx <- createDataPartition(iris$Species, p = 2/3, list = F)
  training_set <- iris[training_idx, ]
  testing_set <- iris[-training_idx, ]

  # create prediction
  training_ctrl <- trainControl(method = "repeatedcv", number = 10, repeats = 3)
  fit <- train(Species ~., data = training_set, method = "knn", trControl=training_ctrl, preProcess = c("center", "scale"), tuneLength = 15)
  prediction  <- predict(fit, newdata = testing_set)

  # examine prediction performance
  print(confusionMatrix(prediction, testing_set$Species))
}
result <- run_prediction_example()