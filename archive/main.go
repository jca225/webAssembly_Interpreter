package main
 
 
func main() {
    fib(47)
}

func fib(n int) int {
    if (n < 2) {
        return n;
    }
    var x = fib(n - 1);
    var y = fib(n - 2);

    return x + y;
}