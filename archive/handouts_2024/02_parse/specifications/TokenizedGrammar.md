# A Grammar for the CSE 262 Version of Scheme

The following grammar is a context-free grammar to define the syntax of our
subset of Scheme.  This grammar produces a **parse tree**, not an **abstract
syntax tree**.  In CSE 262, we never make a parse tree explicitly... our parser
directly produces an AST.  Thus while this parse tree precisely defines which
programs can be *recognized*, it does not correspond, one-to-one, with the
productions that your parser will perform.

This grammar is inspired by <https://www.scheme.com/tspl2d/grammar.html>.

## Productions

The following set of productions defines our grammar.  The `+` and `*` symbols
bind to the item immediately preceding them.

Note that ALLCAPS elements in this grammar refer to specific scanner tokens.

```bnf
<program> --> <form>*

<form> --> <definition> | <expression>

<definition> --> LPAREN DEFINE IDENTIFIER <expression> RPAREN

<expression --> LPAREN QUOTE <datum> RPAREN
              | LPAREN LAMBDA <formals> <body> RPAREN
              | LPAREN IF <expression> <expression> <expression> RPAREN
              | LPAREN SET IDENTIFIER <expression> RPAREN
              | LPAREN AND <expression>+ RPAREN
              | LPAREN OR <expression>+ RPAREN
              | LPAREN BEGIN <expression>+ RPAREN
              | LPAREN COND <condition>+ RPAREN
              | ABBREV <datum>
              | <constant>
              | IDENTIFIER
              | <application>

<condition> --> LPAREN <expression> <expression>* RPAREN

<body> --> <definition>* <expression>

<formals> --> LPAREN IDENTIFIER* RPAREN

<application> --> LPAREN <expression>+ RPAREN

<constant> --> BOOL | INT | DBL | CHAR | STR

<datum> --> BOOL | INT | DBL | CHAR | STR | <symbol>  | <list>  | <vector>

<symbol> --> IDENTIFIER

<list> --> LPAREN <datum>* RPAREN

<vector> --> VEC <datum>* RPAREN

<identifier> --> IDENTIFIER
```

## Other Notes

* The `set!` and `define` special forms are not really expressions.  Later in
  the semester, we will decide what we are going to do about this.
* In `gsi`, `and`, `or`, and `begin` are valid even when they are given zero
  arguments.  Our grammar requires at least one argument.
* This grammar does not include the `else` alias for `#t`
* There are a total of nine keywords: `and`, `or`, `define`, `if`, `cond`,
  `lambda`, `set!`, `begin`, and `quote`, each of which is a "special form".
  `<application>` is the default form.
* Scheme is case-insensitive, but our language is case sensitive.
* Scheme supports arbitrary precision of numbers, but we only support 64-bit
  floating point (double) and 32-bit integer (int) number types.  The grammar
  does not capture that any integer larger than 4294967295 is invalid, or that
  it is possible to craft a double with too many digits.
* The `lambda` special form has some syntactic sugar: You need not use `begin`
  in order to have a lambda with multiple expressions.

---

essential syntax: `lambda <formals> <body>`

Syntax: <Formals> should be a formal arguments list as described below, and <body> should be a sequence of one or more expressions.

Semantics: A lambda expression evaluates to a procedure. The environment in effect when the lambda expression was evaluated is remembered as part of the procedure. When the procedure is later called with some actual arguments, the environment in which the lambda expression was evaluated will be **extended by binding the variables in the formal argument list to fresh locations, the corresponding actual argument values will be stored in those locations, and the expressions in the body of the lambda expression will be evaluated sequentially in the extended environment.** The result of the last expression in the body will be returned as the result of the procedure call.

(lambda (x) (+ x x))        =>  a procedure
((lambda (x) (+ x x)) 4)    =>  8

(define reverse-subtract
  (lambda (x y) (- y x)))
(reverse-subtract 7 10)     =>  3

(define add4
  (let ((x 4))
    (lambda (y) (+ x y))))
(add4 6)                    =>  10
<Formals> should have one of the following forms:

(<variable 1> ...): The procedure takes a fixed number of arguments; when the procedure is called, the arguments will be stored in the bindings of the corresponding variables.
<variable>: The procedure takes any number of arguments; when the procedure is called, the sequence of actual arguments is converted into a newly allocated list, and the list is stored in the binding of the <variable>.
(<variable 1> ... <variable n-1> . <variable n>): If a space-delimited period precedes the last variable, then the value stored in the binding of the last variable will be a newly allocated list of the actual arguments left over after all the other actual arguments have been matched up against the other formal arguments.
It is an error for a <variable> to appear more than once in <formals>.

((lambda x x) 3 4 5 6)      =>  (3 4 5 6)
((lambda (x y . z) z)
 3 4 5 6)                   =>  (5 6)
Each procedure created as the result of evaluating a lambda expression is tagged with a storage location, in order to make eqv? and eq? work on procedures (see section Equivalence predicates).

