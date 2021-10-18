# runs a single testfile and returns results
run_testfile <- function(path, test_list_name = "test_list") {
  test_list <- (function() {source(path, local = TRUE); environment()})()[[test_list_name]] # retrieves test_list variable from testfile # nolint
  test_results <- list()
  for (test_name in names(test_list)) {
    print(paste0("---- test started:", test_name, "----"))
    run_test <- test_list[[test_name]]
    test_results[[test_name]] <- run_test()
    print(paste("---- test complete:", test_name, "----"))
  }
  return(test_results)
}
# results <- run_testfile("/Users/solarapparition/repos/toolkit/R/dummy.R") #nolint
