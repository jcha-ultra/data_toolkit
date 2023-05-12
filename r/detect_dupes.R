# filters a dataframe by records that have duplicate values in a particular column; adapted from original code by Todd-Ultra
detect_dupes <- function(df, colname) {
  n_occur <- data.frame(table(df[[colname]]))
  df[df[[colname]] %in% n_occur$Var1[n_occur$Freq > 1], ]
}