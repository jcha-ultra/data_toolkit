### Some shortcut functions for common combinations of functions

# search for filenames in a zip file based on a pattern and return a vector of the matches. This is just a composition of `unzip` and `grep` for convenience, and any `...` arguments are passed to `grep`
find_names_in_zip <- function(zip_file, pattern, ...) {
    all_file_names <- utils::unzip(zip_file, list = TRUE)
    filtered_names <- grep(pattern, all_file_names$Name, ..., value = TRUE)
    return(filtered_names)
}

# check for 2-way string inclusion
str_includes_2_way <- function(x, y) grepl(x, y) || grepl(y, x)

# return fuzzy version of base R `intersect` with user-supplied equality operator, which can be used to generate equivalent versions for `setdiff` and `setequal`. Do NOT use for performance over large sets, as it is O(n^2)
fuzzy_intersect <- function(a, b, eq) {
  # check if an element `x` is in `b`
  x_in_b <- function(x) purrr::reduce(b, ~.x || eq(.y, x), .init = FALSE)
  a_and_b <- a[purrr::map_lgl(a, x_in_b)]
  return(a_and_b)
}
# test <- fuzzy_intersect(c("blah", "blah2", "b", "d"), c("blah1", "blah3", "a", "c"), str_includes_2_way) # [1] "blah"  "blah2" "b"
