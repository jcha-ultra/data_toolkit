# sources a file when it's updated, otherwise returns memoised result from when it was last run. If this function is redefined, then the previous result will be lost.
run_when_updated <- (function() {
  mem_source <- memoise::memoise(function(file_path, mtime) {
    source(file_path, local = TRUE)
    environment()
  })
  return(function(file_path) {
    mtime <- file.mtime(file_path)
    source_data <- mem_source(file_path, mtime)
    return(source_data)
  })
})() # IIFE
# test <- run_when_updated("file_path/script.R")