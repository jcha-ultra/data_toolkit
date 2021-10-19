### Some shortcut functions for common variations of functions

# search for filenames in a zip file based on a pattern and return a vector of the matches. This is just a composition of `unzip` and `grep` for convenience, and any `...` arguments are passed to `grep`
find_names_in_zip <- function(zip_file, pattern, ...) {
    all_file_names <- utils::unzip(zip_file, list = TRUE)
    filtered_names <- grep(pattern, all_file_names$Name, ..., value = TRUE)
    return(filtered_names)
}

# check for 2-way string inclusion
str_includes_2_way <- function(x, y) grepl(x, y) || grepl(y, x)

# find all elements in `a` that has an equivalent in `b`, with equivalence as defined by `eq`. This is NOT commutative, as it will only return the version of the element found in `a`. Do not use for large sets, as it is O(n^2)
# for more comprehensive and performant functionality, use the `fuzzyjoin` package: https://cran.r-project.org/package=fuzzyjoin
fuzzy_intersect <- function(a, b, eq) {
  # check if an element `x` is in `b`
  x_in_b <- function(x) purrr::reduce(b, ~.x || eq(.y, x), .init = FALSE)
  a_and_b <- a[purrr::map_lgl(a, x_in_b)]
  return(a_and_b)
}
# test <- fuzzy_intersect(c("blah", "blah2", "a", "c"), c("blah1", "blah3", "b", "d"), str_includes_2_way)
# expected: `[1] "blah"  "blah2" "a"`; note that reversing the order of the arguments will result in `[1] "blah1" "blah3" "b"` instead
