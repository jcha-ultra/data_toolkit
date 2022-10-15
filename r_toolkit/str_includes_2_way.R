# check for 2-way string inclusion
str_includes_2_way <- function(x, y) grepl(x, y) || grepl(y, x)