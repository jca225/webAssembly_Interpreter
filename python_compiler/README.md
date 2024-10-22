# Overview

"Musicians play their instruments. I play the orchestra."
― Steve Jobs

## Concepts
WebAssembly encodes a low-level, assembly-like programming language. This language is strutured around the following concepts:

### Values
+ WebAssembly provides only four bassic number types, each 32 and 64 bits. 
+ 32 bit integers also serve as Booleans and as memory addresses
+ There is no distinction between signed an unsigned integer types. Instead, integers are interpreted by respective operations as either signed or unsigned in two's complement representation.
+ There is also a single 128 bit wide vector type representing different types of packed data.
+ Values can also consist of opaque references that represent pointers toward different sorts of entities.
    + Unlike with other types, their size or representation is not observable

### Instructions
+ The computational model of WebAssembly is based on a *stack machine*
+ Instructions are executed sequentially
    + Simple instructions perform basic operations on data; They pop arguments from the operand stack and push results back to it
    + Control instructions alter control flow. Control flow is *structured*, meaning it is expressed with well-nested constructs such as blocks, loops, and conditionals. Branches can only target such constructs

### Traps
+ Under some conditions, certain instructions may produce a trap, which ammediately abords execution. 
+ Traps cannot be handled by WebAssembly code, but are reported to the outside environment, where they typically can be caught.

### Functions
+ Code is organized into separate functions. Each function takes a sequence of values as parameters and returns a sequence of values as a result. 
+ Functions can call each other, including recursively, resulting in an implicit call stack that cannot be accessed directly.
+ Functions my also declar mutable local variables that are usable as virtual registers,
Example of vector of parameters:
```(func (param i32) (param i32) (result f64) ...)````
=> `(param i32) (param i32)` == `vec(param)`
### Tables
+ A table is an array of opaque values of a particular element type
+ A program can call functions indirectly through a dynamic index into a table
     + This allows emulating function pointers by way of table indices.

### Linear Memory
+ Contiguous, mutable array of raw bytes. 
+ Created with an initial size but can grow dynamically. 
+ A trap occurs if an access is not within the bounds of the current memory size


### Modules
+ A WebAssembly binary takes the form of a *module* that contains definitions for functions, tables, and linear memories, as well as mutable or immutable global variables. 
+ Definitions can also be imported, specifying a module/name pair and a suitable type
+ Each definition can be optionally exported under one or more names

### Embedder
+ A WebAssembly implementation will typically be embedded into a host environment. 


# Lexical Format

## Characters
The text format assigns meaning to source text. Characters are assumed to be represented as valid unicode:
source ::= char*
char   ::= U+00 | ... | U+D7FF | ... | U+10FFFF


## Tokens
token     ::= keyword | uN | sN | fN | string | id | '(' | ')' | reserved
keyword   ::= ('a' | ... | 'z') idchar*
reserved  ::= (idchar|string)+


## White Space
White space is any sequence of literal space characters, formatting characters, or comments.
The only use of white space is to separate tokens. It is otherwise ignored

space   ::= (' ' | format | comment)*
format  ::= newline|U+09
newline ::= U+0A | U+0D | U+0A U+0D 

Note: The U+XX implies that the byte should be read as unicode:
U+0A = '\n'
U+09 = '\'
U+0D = '\r'

## Control Instructions
Structured control instructions can bind an optional symbolic label identifier. The same label identifier may optionally be repeated after the corresponding `end` and `else` pseudo instructions, to indicate matching delimiters. 
Their block type is given as a type use, analogous to the type of functions. However, the special case of a type use that is syntactically empty or consists of only a single result is not regarded as an abbreviatyion for an inline function type, but is parsed directly into an optional value type.

## Contexts
The text format allows the use of symbolic identifiers in place of indices. To resolve these identifiers into concrete
indices, some grammar productions are indexed by an *identifier context I* as a synthesized attribute that records the declared identifiers in each index space. In addition, the context records the type defined in the module, so that parameter indices can be computed for functions. 
We define identifier contexts as records I with abstract syntax as follows"

I   ::=   { types    (id^?)*,
            funcs    (id^?)*,
            tables   (id^?)*,
            mems     (id^?)*,
            globals  (id^?)*,
            elem     (id^?)*,
            data     (id^?)*,
            locals   (id^?)*,
            labels   (id^?)*,
            typedefs *functype*}

For each index space, such a context contains the list of identifers assigned to the defined indices. Unnamed indices are associated with empty (\epsilon) entries in these lists. 

An identifier context is *well-formed* if no index space contains duplicate identifiers

## Control Instructions
Instructions in this group affect the flow of control

blocktype   ::= *typeidx* | *valtype*^?
instr       ::= ...
             |  nop
             |  unreachable
             |  block *blocktype* *instr* * end
             |  loop *blocktype* *instr* * end
             |  if *blocktype* *instr* * else instr* end
             |  br *labelidx*
             |  br_if *labelidx*     
             |  br_table vec(*labelidx*) *labelidx*
             |  return
             |  call *funcidx*
             |  call_indirect *tableidx* *typeidx*       

The `nop` instruction does nothing
The `unreachable` instruction causes an unconditional `trap`

## Labels
Structured control instructions can be annotated with a symbolic label identifier. They are the only symbolic identifiers that can be bound locally to an instruction sequence. 
The following syntax allows us to add identifiers to our record *I* above. 
label_*I*  ::=  v:id  =>  {labels v} \+ *I*                         (if*I*.labels[i] = v)
            |   v:id  =>  {labels v} \+ (*I* with labels[i] = \ep)  (if*I*.labels[i] = v)
            |   \ep   =>  {labels(\ep)} \+ *I*


**Note**: The new label entry is inserted at the *beginning* of the label list in the identifier context. This effectively shifts all existing labels up by one, mirroring the fact that the control instructions are indexed relatively not absolutely. 
**If a label with the same name already exists, then it is shadowed and the earler label becomes inaccessible**
## Vectors
Vectors are written as plain sequences, with a restriction on the length of the sequence

vec(A)  ::= (x:A)^n => x^n     (if n < 2^{32})


## Identifiers
Indices can be given both numeric and symbolic form.
Symbolic identifiers that stand in lieu of numeric identifiers start with '$', followed by a sequence of ASCII characters.
None of these can be a space, quotation mark, comma, semicolon, or bracket
numbers = list(range(10))
print(numbers)  # Output: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

## Instructions
Instructions are syntactically distinguished into *plain* and *structured* instructions

## Tokens
The character stream in the source text is divided, from left to right, into a sequence of tokens, as defined by the following grammar.
token    ::= keyword| u𝑁 |s𝑁 |f𝑁 |string|id|‘(’|‘)’|reserved
keyword  ::= (‘a’ | . . . | ‘z’) idchar* (if occurring as a literal terminal in the grammar)
reserved ::= (idchar | string)+

Tokens are formed from the input character stream according to the *longest match rule*. That is, the next token always consists of the longest possible sequence of characters that is recognized by the above lexical grammar. Tokens can be separated by white space, but **except for strings**, they cannot themselves contain whitespace.
Keyword tokens are defined either implicitly by an occurrence of a terminal symbol in literal form, such as ‘keyword’, in a syntactic production of this chapter, or explicitly where they arise in this chapter.
Any token that does not fall into any of the other categories is considered reserved, and cannot occur in source text.
Note: The effect of defining the set of reserved tokens is that all tokens must be separated by either parentheses, white space, or comments. For example, ‘0$x’ is a single reserved token, as is ‘”a””b”’. Consequently, they are not recognized as two separate tokens ‘0’ and ‘$x’, or ”𝑎” and ”𝑏”, respectively, but instead disallowed. This property of tokenization is not affected by the fact that the definition of reserved tokens overlaps with other token classes.

## Indices
Indices can be given either in raw numeric form or as symbolic identifiers when bound by a respective construct. Such identifiers are looked up in the suitable space of the identifier context *I*.

typeidx_I    ::= x:u32 => x
              |  v:id  => x (if I.types[x] = v)
funcidx_I    ::= x:u32 => x 
              |  v:id  => x (if I.funcs[x] = v)
tableidx_I   ::= x:u32 => x
              |  v:id  => x (if I.tables[x] = v)
memidx_I     ::= x:u32 => x
              |  v:id  => x (if I.mems[x] = v)
globalidx_I  ::= x:u32 => x
              |  v:id  => x (if I.globals[x] = v)
elemidx_I    ::= x:u32 => x
              |  v:id  => x (if I.elem[x] = v)
dataidx_I    ::= x:u32 => x
              |  v:id  => x (if I.data[x] = v)
localidx_I   ::= x:u32 => x
              |  v:id  => x (if I.locals[x] = v)
labelidx_I   ::= x:u32 => x 
              |  v:id  => x (if I.labels[x] = v)

## Modules
A module consists of a sequence of fields that can occur in any order. All definitions and their respective bound identifiers scope over the entire module, including the text preceding them.

# Invariants
1. Increments must bring us to the smallest index containing the value that has not been parsed yet



C: two environments: local, global
But what about functions in functions?
    Does WebAssembly support this?
Really complex scoping: Environments that have reference to other environments
Functions close over by keeping track of that environment
Callstack of environments

Read Bytecode
.class -> javap to print its bytecode
Java compiler knows all of the local variables and has an efficient way of representing them.
Three categories of language with source -> execution:

None of these are turing complete
1. regular languages   
    a. Recognize a b a
                a b^n a
    But can you get a b^n c^n d
    Regular language cannot remember a number long enough to use it later -- memoryless
    Regex basically the same thing


2. parsing
    a. Context-Free Grammar: A language that does not have very much to keep track of -- what i do with the next thing only depends on a 
       very small and fixed amount of things. 
       "a b^n c^n d" is possible because it is not just a linear scan; we have a notion of a stack. Pushing for b, popping for c, and if we don't get the right value, then we know its invalid. 
       A little bit but not enough; context-sensitive gets you even more.
       Programming Languages require some amount of expression that is more robust than a context-free grammar.

    
1. Regular language -> token
2. Context free -> parsing
    a. Paring just gives you a tree, "here is another way to think about it"
3. Context sensitive -> input a parse-tree
    a. Do we want to analyze w.r.t errors or warnings? 
    Not much you can do for errors with parsing.
    Separate information outside the sphere of the parse tree to see if things far away make sense
    Sake of correctness or sake of optimality.
    Static and non-static fields, create struct with a slot for each of those things
    Then we can go through all accesses and categorize them.
    Does this name refer to something, what does it refer to, and now we have class statics, instance fields, and all local variables.
    All of the data accesses become local.6, instance.7, or static.9. Now when it comes time to execute there are no hash-table look-ups. 
    It is a direct index into a specific spot in a struct. 
    Transformed into a more desirable AST
4. Turing complete 



Just trying to run the webassembly, we don't need to typecheck and we can just assume typecheck.



Vector of expressions

Function call 

What are the different formats for addition?
1. 
```
(i32.add ($a) ($b))
```
```
i32.add
```




# Evaluating
`x` is a local variable of the function
the JVM makes a struct that will have a field called `x`.
Local variable definitions -- not all of them are on the stack; some of them are in some auxiliary structure.
The local.get instruction loads the value of a local variable onto the stack.
Page 26 - validation for dealing with locals

The implementation of the interpreter
Tail-recursion:
Push new env onto the stack, make note it needs to pop
Overwrite this environment with a new environment.
Make new environment chain to the previous one.
Produce new, get rid of old, and swap the two.
New local variables are not related to the locals of the previous one.
Pass over the bytecode first.
every time you get to a function, you could go through this function, 
and look at all the local variable operations. Use them to build some local
variable meta data for the function.
How many locals, their types.
Set up struct each of which has the corresponding variables.
Big performance boost.
Make an efficient local frame
Meta-data included information so we did not have to scan through the function to figure it out.
Move to Go
Concurrency
Extend with Spawn and Sync
A lot of nasty 
Symbol tables, stackframes in Dragon Compiler
We have to make the stack frame ahead of time so the threads runningthis
race free program are not racing inside the interpreter initializing the stack frame


Memory: create array

Build up enough infrastructure to study the problem

The key is to compile 