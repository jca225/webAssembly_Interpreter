# The CSE 262 "Slang" Standard Library

Below is a list of all the functions you should implement for your standard
library.  They are broken into four categories (Vector, List, String, and Math).
There are also some math constants.

The function names should be pretty self-explanatory.  The arguments should also
be self-explanatory.  Note that `val` means "any IValue", and `vals...` either
means zero-or-more or one-or-more.

Please note that for the most part, these functions behave the same as in `gsi`.
For example, `(- 10 3 4)` should return `3`, and `(> 1 2)` should return `#f`.

## Vector Functions

* `(vector-length vec)`
* `(vector-get vec idx)`
* `(vector-set! vec idx val)`
* `(vector vals...)` (zero or more values)
* `(vector? val)`

## List Functions

* `(car cons-cell)`
* `(cdr cons-cell)`
* `(cons val1 val2)`
* `(list vals...)` (zero or more values)
* `(list? val)`
* `(set-car! cons val)`
* `(set-cdr! cons val)`

## String Functions

* `(string-append str str)`
* `(string-length str)`
* `(substring str fromInc toExc)` (fromInc and toExc are integers; first is inclusive, second is exclusive)
* `(string? val)`

## Math Functions

* `(+ number...)` (one or more values)
* `(- number...)` (one or more values)
* `(* number...)` (one or more values)
* `(/ number...)` (one or more values)
* `(% number...)` (one or more values)
* `(== number...)` (one or more values)
* `(> number...)` (one or more values)
* `(>= number...)` (one or more values)
* `(< number...)` (one or more values)
* `(<= number...)` (one or more values)
* `(abs number)`
* `(sqrt number)`
* `(acos number)`
* `(asin number)`
* `(atan number)`
* `(cos number)`
* `(cosh number)`
* `(sin number)`
* `(sinh number)`
* `(tan number)`
* `(tanh number)`
* `(integer? number)`
* `(double? number)`
* `(number? number)`
* `(symbol? number)`
* `(procedure? number)`
* `(log10 number)`
* `(loge number)`
* `(pow baseNum expNum)`
* `(not val)`
* `(integer->double int)`
* `(double->integer double)`
* `(null?)`
* `(and vals...)` (one or more values)
* `(or vals...)` (one or more values)

## Math Constants

* `pi`
* `e`
* `tau`
* `inf+`
* `inf-`
* `nan`
