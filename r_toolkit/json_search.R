#' Recursively finds paths to values that match the given value in a JSON object
#' @param object A JSON object
#' @param value The value to find
#' @return A list of paths to values that match the given value
#' @export
#' @examples
#' search_for_value_paths(jsonlite::fromJSON('{"a": {"b": {"c": 1}}, "d": 1}'), 1)
#' [[1]]
#' [1] "a" "b" "c" "1"
#'
#' [[2]]
#' [1] "d" "1"
search_for_value_paths <- function(object, value) {
  # print(object)
  if (is.null(object)) {
    return(list())
  } else if (is.list(object)) {
    paths <- list()
    for (key in names(object)) {
      for (path in search_for_value_paths(object[[key]], value)) {
        paths <- c(paths, list(c(key, path)))
      }
    }
    return(paths)
  } else if (is.vector(object)) {
    return(list(which(object == value)))
  }
}
test_search_for_value_paths <- search_for_value_paths(jsonlite::fromJSON('{"a": {"b": {"c": 1}}, "d": 1}'), 1)

