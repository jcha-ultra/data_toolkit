# These two functions implement tail-call optimization in R; for more information, see https://tailrecursion.com/wondr/posts/tail-recursion-in-r.html

trampoline <- function(f, ...) {
  function(...) {
    ret <- f(...)
    while (inherits(ret, "recursion")) {
      ret <- eval(as.call(c(f, unclass(ret))))
    }
    ret
  }
}
recur <- function(...) {
  structure(list(...), class = "recursion")
}

# usage: wrap the function to be recursed inside the `trampoline` function, then replace all recursive calls inside the function with calls to `recur`, with the same arguments

# example:
# countdown <- trampoline(function(n) {
#   if (n > 0) recur(n-1) else "done"
# })
