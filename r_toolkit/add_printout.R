# add printout functionality to a function; `print_start` and `print_end` are functions that return values to be printed out at the start and end respectively, and will be passed the parameters to the main function; `print_end` will also be given the value of the function's return value
add_printout <- function(f, print_start, print_end) {
  return(function(...) {
    print(print_start(...))
    val <- f(...)
    print(print_end(val, ...))
    return(val)
  })
}
# f <- function(a, b) a + b; f_w_printout <- add_printout(f, function(a, b) a, function(val, ...) val) # example