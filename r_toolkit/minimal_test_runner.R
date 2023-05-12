### These functions provide a very basic test runner that will run some testfiles and return results from the tests
# - for more robust testing functionality, the `testthat` package is recommended: https://testthat.r-lib.org/
# - this test runner has very little functionality, but it has no package dependencies, and can incorporate any test script with minimal modification

# run a single testfile and returns results; testfiles can be any R script, but must set a variable that has the same name as `test_list_name` that is a list of 0-argument test functions
run_testfile <- function(path, test_list_name = "test_list") {
  test_list <- (function() {source(path, local = TRUE); environment()})()[[test_list_name]] # retrieves test_list variable from testfile
  test_results <- list()
  for (test_name in names(test_list)) {
    print(paste0("----test started: ", test_name, "----"))
    run_test <- test_list[[test_name]]
    test_results[[test_name]] <- run_test()
    print(paste0("----test complete: ", test_name, "----"))
  }
  return(test_results)
}
# results <- run_testfile("~/repos/toolkit/R/dummy.R")


# run all testfiles in provided list and save their results in their own bucket
run_tests <- function(testfiles, test_dir, testfile_runner = run_testfile) {
  print("--tests started!--")
  all_test_results <- list() # list that holds all test results
  for (filename in testfiles) {
    print(paste0("---testfile started: ", filename, "---"))
    path <- paste0(test_dir, "/", filename)
    testfile_results <- testfile_runner(path)
    all_test_results[[filename]] <- testfile_results
    print(paste0("---testfile complete: ", filename, "---"))
  }
  print("--all tests complete!--")
  return(all_test_results)
}
# results <- run_tests("dummy.R", "~/repos/toolkit/R", run_testfile)

# Example testfile:
# test_list <- list()
# test_list$test_1 <- function() {return("test was run!")}