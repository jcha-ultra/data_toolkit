# Julia closure example
function adder(x, a)
    return a->x+a
end

function add_a(x) return adder(x, a) end


# piping inputs to 2nd parameters
function print_2nd(first, second) print(second) end
value = "bar"

value |> (x) -> print_2nd(nothing, x)


# calculates the inverse sum of the fibonacci(ish) sequence, starting with 1/2, i.e. 1/2 + 1/3 + 1/5 + ...: 
fib_inv_sum = (function () prev_1 = 1; prev_2 = 1; sum = 0; function() next = prev_1 + prev_2; sum = sum + 1/next; prev_1 = prev_2; prev_2 = next; return sum end end)()
