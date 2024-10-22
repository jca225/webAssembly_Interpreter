# Notes on the implementation of the Compiler:
1. `\n` does not necessarily matter; we are only concerned with the S-expressions, which are mainly dictated by parentheses
2. The fundamental unit of code in Web Assembly is a module 