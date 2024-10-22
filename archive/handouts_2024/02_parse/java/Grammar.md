# A Grammar for our Version of Scheme

This grammar is inspired by <https://www.scheme.com/tspl2d/grammar.html>.

## Productions

The following (not entirely formal) set of productions defines our grammar:

```bnf
<program> -> <form>*

<form> -> <definition> | <expression>

<definition> -> (define <identifier> <expression>)

<expression -> (quote <datum>)
             | (lambda <formals> <body>)
             | (if <expression> <expression> <expression>)
             | (set! <identifier> <expression>)
             | (and <expression>+)
             | (or <expression>+)
             | (begin <expression>+)
             | (cond (<expression> <expression>*)*)
             | '<datum>
             | <constant>
             | <identifier>
             | <application>

<body> -> <definition>* <expression>

<formals> -> (<identifier>*)

<application> -> (<expression>+)

<identifier> -> <initial><subsequent>*| + | -

<initial> -> <letter> | ! | $ | % | & | * | / | : | < | = | > | ? | ~ | _ | ^

<subsequent> -> <initial> | <digit> | . | + | -

<letter> -> <any character from a to z, uppercase or lowercase>

<digit> -> <any character from 0 to 9>

<constant> -> <boolean> | <number> | <character> | <string>

<datum> -> <boolean> 
         | <number> 
         | <character> 
         | <string> 
         | <symbol> 
         | <list> 
         | <vector>

<boolean> -> #t | #f

<character> -> #\<any single-byte character that isn't whitespace> 
             | #\newline 
             | #\space 
             | #\tab

<string> -> "<string character>*"

<string character> -> \" 
                    | \\ 
                    | \t 
                    | \n 
                    | <any character other than `"` or `\`>

<symbol> -> <identifier>

<list> -> (<datum>*)

<vector> -> #(<datum>*)

<number> -> <sign> <real>

<real> -> <integer> | <decimal>

<integer> -> <digit>+

<decimal> -> <digit>+ . <digit>+

<sign> -> <empty> | + | -
```

## Notes

* For brevity, some of these productions are not true EBNF form.  For example,
  `cond` really ought to have a sub-rule for each of its sets of expressions.
* The `<identifier>` production may look strange: we need special care, because
  `+` and `-` can be single-character identifiers, and can appear in the middle
  of identifiers, but can also be the first character (`<sign>`) of a number.
  Thus they cannot be the first character of a multi-character identifier.
* The `set!` and `define` special forms are not really expressions.  Later in
  the semester, we will decide what we are going to do about this.
* Scheme is case-insensitive, but our language is case sensitive.
* Scheme supports arbitrary precision of numbers, but we only support 64-bit
  floating point (double) and 32-bit integer (int) types.  The grammar does not
  capture that any integer larger than 4294967295 is invalid, or that it is
  possible to craft a double with too many digits.
* In `gsi`, `and`, `or`, and `begin` are valid even when they are given zero
  arguments.
* This grammar does not include the `else` alias for `#t`
* There are a total of nine keywords: `and`, `or`, `define`, `if`, `cond`,
  `lambda`, `set!`, `begin`, and `quote`, each of which is a "special form"
  (`<application>` is the default form).
  