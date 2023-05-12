# search for filenames in a zip file based on a pattern and return a vector of the matches. This is just a composition of `unzip` and `grep` for convenience, and any `...` arguments are passed to `grep`
find_names_in_zip <- function(zip_file, pattern, ...) {
    all_file_names <- utils::unzip(zip_file, list = TRUE)
    filtered_names <- grep(pattern, all_file_names$Name, ..., value = TRUE)
    return(filtered_names)
}