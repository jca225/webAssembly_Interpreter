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

Note that ALLCAPS elements in this grammar refer to specific sanner tokens.

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
