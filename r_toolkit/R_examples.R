
# > r: exists: checks if object exists
# > r: stopifnot: stopifnot("Configuration variables not set. Please run `config.R`" = exists("CONFIG_SET"))


# function documentation example:

#' Add together two numbers
#'
#' @param x A number.
#' @param y A number.
#' @return The sum of \code{x} and \code{y}.
#' @examples
#' add(1, 1)
#' add(10, 1)
# add <- function(x, y) {
#   x + y
# }


# formula examples
y ~ x + 1 # bare formula
~ x + 1 # it's possible to only have the righthand side

stats::lm(y ~ x + 1, data = some_data) # how a formula would typically be used as an input; here x and y are column variables of `some_data`

stats::lm(y ~ ., data = some_data) # the dot here means "all columns not in the rest of the formula", so all columns in `some_data` that is not y

purrr::map(list(1, 2, 3), ~.x + 1) # example of rhs-only formula being used by a function


# piping inputs to 2nd parameters
library(magrittr)
print_2nd <- function(first, second) print(second)
value <- "foo"

value %>% 
  (function(x) print_2nd(NULL, x))()
  
# NOTE: probably best to use magrittr's built-in dot notation for this instead:
value %>% print_2nd(NULL, .)


# vroom materialization testing

# generate table with vroom vectors
set.seed(42)
types <- "cidTD"
x <- vroom::gen_tbl(10, 5, col_types = types)
readr::write_tsv(x, "altrep.tsv")
y <- vroom::vroom("altrep.tsv", col_types = types)

.Internal(inspect(y$X1)) # `materialized=F` initially
y$X1 # evaluate the vector
.Internal(inspect(y$X1)) # `materialized=T` now because we evaluated `y$X1`

.Internal(inspect(y$X2)) # other vectors are not materialized until they're evaluated

y$X1[seq_len(nrow(y))] # "subset" the length of the entire vector
.Internal(inspect(y$X1)) # will NOT materialize even though we subsetted every element

x_1 <- y$X1 # assign to another variable
.Internal(inspect(x_1)) # still not materialized due to R's copy-on-modify semantics

y$X1[1] <- "foo" # will convert X1 into a regular, non-altrep vector
.Internal(inspect(y, 1))

z <- dplyr::filter(y, X1 == "icuMPaw") # perform some arbitrary filter
.Internal(inspect(z, 1)) # will NOT materialize any vectors

w <- dplyr::group_by(y, X1)
.Internal(inspect(w)) # WILL materialize; see [1]


# object copying in R
a1 <- list(1, 2, 3)
cat(tracemem(a1), "\n")
a2 <- a1 # tracemem does NOT detect a copy

b1 <- list(1, 2, 3)
cat(tracemem(b1), "\n")
b1[[4]] <- 4 # tracemem DOES detect a copy

d <- list(1, 2, 3)
cat(tracemem(d), "\n")
foo <- function(x) x
foo(d) # tracemem does NOT detect a copy


# lazy eval
foo <- function(x) {
  print("this happened")
  return(x)
}
foo(stop()) # WILL print, because `x` is not evaluated until the `return` statement

bar <- function(x) {
  x
  print("this happened") 
  return(x)
}
bar(stop()) # will NOT print because `stop()` is evaluated before the `print` statement

baz <- function(x) {
  print("yup still works")
}
baz(this(aint(evaluated))) # will still print as long as the argument is a legal form

# generic function demo

# define the generic; it's just a function with a single call to `UseMethod`
plus2 <- function(x) {
  UseMethod("plus2")
}

# figure out class names for a few example objects
class(3L) # "integer"
class(3.5) # "numeric"
class("3") # "character"

# define the method for class "integer"; note the dot separator in the function name
plus2.integer <- function(x) {
  x + 2
}
plus2(5L) # 7
plus2(5) # wouldn't work because "numeric" method is not defined yet

# define method for "numeric"
plus2.numeric <- function(x) {
  x + 2
}
plus2(5) # 7.0

# define method for "character"
plus2.character <- function(x) {
  as.numeric(x) + 2
}
plus2("5") # 7

# define default method when no method was found for argument class
plus2.default <- function(x) {
  print("why would you do this")
}
plus2(list()) # why would you do this


# creating confusion matrix from predicted and actual values
table(actual, predicted)
   
#      0   1
#  0 524  25
#  1 115 227


# viewing function source code
# user-defined function
foo <- function() print("nothing")

foo
# output:
# function() print("nothing")

# you can also view the source code of a function in a package
dplyr::add_row

# if a package function is not exported, use the ::: operator
dplyr:::arg_name


# printout options:

# regular print
> print(c("foo", "bar"))
[1] "foo" "bar"

# remove quotes
> noquote(c("foo", "bar"))
[1] foo bar

# remove quotes and index, and print out in separate lines
> write(c("foo", "bar"), stdout())
foo
bar


# curve example
curve((x-5)^2+3, from = 0, to = 10, ylab = "loss", xlab = "parameter (m)")
