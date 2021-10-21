# These two functions implement tail-call optimization in R; for more information, see https://tailrecursion.com/wondr/posts/tail-recursion-in-r.html

# usage: wrap the function to be recursed inside the `trampoline` function, then replace the recursive call inside the function with calls to `recur`, with the same arguments

# example:
# countdown <- trampoline(function(n) {
#   if (n > 0) recur(n-1) else "done"
# })

trampoline <- function(f, ...) {
  function(...) {
    ret <- f(...)

    # keep calling `f` as long as the base case hasn't been reached yet
    while (inherits(ret, "recursion")) {
      ret <- eval(as.call(c(f, unclass(ret))))
    }
    ret
  }
}

# returns arguments given with additional indication that further recursion is necessary
recur <- function(...) {
  structure(list(...), class = "recursion")
}
