#include <iostream>

extern "C" {
    int fib(int n) {
        if (n < 2) {
            return n;
        }
        int x = fib(n - 1);
        int y = fib(n - 2);

        return x + y;
    }
}


int main() {
    // This is a dummy main function to satisfy the linker.
    return 0;
}