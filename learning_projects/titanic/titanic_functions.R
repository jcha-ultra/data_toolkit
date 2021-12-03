# This file contains an extraction of the functions in `titanic.Rmd`, so that they're usable elsewhere

clean_titanic_data <- function(df, has_Survived_col = TRUE) {
  data_cleaned <- subset(df, select = -c(PassengerId, Name))
  if (has_Survived_col)
    data_cleaned[["Survived"]] <- as.factor(data_cleaned[["Survived"]])
  return(data_cleaned)
}

encode_titanic_data <- function(df) {
  training_data_encoded <- df
  training_data_encoded$Sex <- encode_sex(df$Sex)

  # training_data_encoded$Survived <- as.integer(as.character(training_data_encoded$Survived))

  # target encoding
  encoded_cols <- c("Ticket", "Cabin", "Embarked")
  encoding <- training_data_encoded %>%
    mutate(Survived = as.integer(as.character(Survived))) %>%
    build_target_encoding(cols_to_encode = encoded_cols, target_col = "Survived")
  training_data_encoded <- target_encode(training_data_encoded, target_encoding = encoding) %>% select(!all_of(encoded_cols))
  return(training_data_encoded)
}

encode_sex <- function(coldata) purrr::map_int(coldata, function(x) if(x == "male") 1L else 0L)

impute_by_mean <- function(df, col_name) {
  df[[col_name]][is.na(df[[col_name]])] <- mean(df[[col_name]], na.rm=TRUE)
  return(df[[col_name]])
}

impute_titanic_data <- function(df) {
  col_to_impute <- "Age"
  training_data_imputed <- df
  training_data_imputed[[col_to_impute]] <- impute_by_mean(df, col_to_impute)
  return(training_data_imputed)
}

prep_training_data <- function(raw_data) {
  data_cleaned <- clean_titanic_data(raw_data, has_Survived_col = TRUE)
  data_encoded <- encode_titanic_data(data_cleaned)
  data_imputed <- impute_titanic_data(data_encoded)
  data_prepped <- subset(data_imputed, select = -c(Survived_mean_by_Ticket, Survived_mean_by_Cabin))
  return(data_prepped)
}

pca_titanic_data <- function(data) {
  # data <- training_data_prepped # debug
  training_data_predictors <- select(data, all_of(setdiff(colnames(data), "Survived")))
  predictors_pca <- prcomp(training_data_predictors, center = TRUE, scale. = TRUE)
  return(predictors_pca)
}

rotate_training_data <- function(data, data_pca, drop = 6:7) {
  rotated_predictors <- data_pca$x
  rotated_predictors_drop <- rotated_predictors[, -drop]
  training_data_pca_rotated <- cbind(as.data.frame(rotated_predictors_drop), Survived = data$Survived)
  return(training_data_pca_rotated)
}

prep_testing_data_2 <- function(raw_data, training_data_encoded) {
  testing_data_prepped <- subset(raw_data, select = -c(PassengerId, Name, Ticket, Cabin))
  testing_data_prepped$Sex <- encode_sex(testing_data_prepped$Sex)
  encoding_map <- data.frame(Embarked = training_data$Embarked, Survived_mean_by_Embarked = training_data_encoded$Survived_mean_by_Embarked) %>% unique()
  testing_data_prepped$Survived_mean_by_Embarked <- purrr::map_dbl(testing_data_prepped$Embarked, function(emb_val) encoding_map$Survived_mean_by_Embarked[[which(encoding_map$Embarked == emb_val)]])
  testing_data_prepped$Age <- impute_by_mean(testing_data_prepped, "Age")
  testing_data_prepped$Fare <- impute_by_mean(testing_data_prepped, "Fare") # new; no NAs in training data
  return(testing_data_prepped)
}

rotate_testing_data <- function(data, data_pca, drop = 6:7) {
  # data_pca <- training_data_pca
  # data <- testing_data_prepped
  rotated_predictors <- predict(data_pca, newdata = data)
  rotated_predictors_drop <- rotated_predictors[, -drop]
  testing_data_pca_rotated <- as.data.frame(rotated_predictors_drop)
  return(testing_data_pca_rotated)
}

train_titanic_model <- function(training_df, seed = NULL) {
  if (!is.null(seed)) set.seed(seed)
  # create prediction
  training_ctrl <- trainControl(method = "cv", number = 10)
  fit <- train(Survived ~ ., data = training_df, method = "knn", trControl=training_ctrl, preProcess = c("center", "scale"), tuneLength = 15)
  return(fit)
}

predict_titanic <- function(training_df, test_df, seed = NULL) {
  prediction <- predict(train_titanic_model(training_df), newdata = test_df)
  # temp1.1 <<- training_df # debug
  # temp1 <<- train_titanic_model(training_df, seed) # debug

  # examine prediction performance
  # print(test_df$Survived)
  if(!is.null(test_df[["Survived"]])) print(confusionMatrix(prediction, test_df[["Survived"]]))
  return(prediction)
}

write_titanic_prediction <- function(prediction, testing_data, name) {
  prediction_df <- data.frame(PassengerId = testing_data$PassengerId, Survived = prediction)
  write.csv(prediction_df, paste0("~/repos/toolkit/learning_projects/titanic/", name), row.names = FALSE)
}

# pacman::p_load(caret, dataPreparation, magrittr, dplyr)
# training_data <- read.csv("~/repos/toolkit/datasets/titanic/train.csv")
# testing_data <- read.csv("~/repos/toolkit/datasets/titanic/test.csv")
# seed <- 3000
# training_data_prepped <- prep_training_data(training_data)
# training_data_rotated <- rotate_training_data(training_data_prepped, training_data_pca)
# training_data_cleaned <- clean_titanic_data(training_data)
# training_data_encoded <- encode_titanic_data(training_data_cleaned)
# testing_data_prepped <- prep_testing_data_2(testing_data, training_data_encoded)
# testing_data_rotated <- rotate_testing_data(testing_data_prepped, training_data_pca)
# predicted_Survived_testing <- predict_titanic(training_data_rotated, testing_data_rotated, seed = seed)
# write_titanic_prediction(predicted_Survived_testing, testing_data, "titanic_prediction_pca.csv")
