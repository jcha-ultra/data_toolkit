# flag values that could potentially represent missing data
flag_missing <- function(coldata) {
  badvals <- c(
    "n/a",
    "na",
    "not available",
    "incomplete",
    "unknown",
    "null",
    "nil",
    "not provided",
    "*"
  )
  colvals <- unique(coldata)
  dr_badvals_found <- dataReporter::identifyMissing(colvals)$problemValues   # [use data reporter's identifyMissing function as basis]
  badvals_found <- as.character(colvals)[tolower(as.character(colvals)) %in% badvals]
  all_badvals_found <- c(dr_badvals_found, badvals_found)
  class(all_badvals_found) <- "missing_flagged"
  return(all_badvals_found)
}

# add printout for result
print.missing_flagged <- function(x) {write(paste0("Potential values representing missing data: \"", paste(x, collapse = "\", \""), "\""), stdout()); x}

# tests
res <- flag_missing(c("N/A","Not Available","incomplete","unknown","null","nil", "not provided"," ","99999999", "*", "-", "sadfasdfa", "foo", "bar"))
testthat::expect_equal(as.character(res), c("-", "99999999", " ", "N/A", "Not Available", "incomplete", "unknown", "null", "nil", "not provided", "*"))