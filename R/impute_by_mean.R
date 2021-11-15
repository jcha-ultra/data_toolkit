
# imputes missing numerical values by mean of the non-missing values
impute_by_mean <- function(df, col_name) {
  df[[col_name]][is.na(df[[col_name]])] <- mean(df[[col_name]], na.rm = TRUE)
  return(df[[col_name]])
}
