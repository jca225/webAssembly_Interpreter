## Modules

module      --> '(' 'module' id^? (m:modulefield)* ')'

moduelfield --> type
                import
                func
                table
                mem
                global
                export
                start
                elem
                data




I   -->   types    (id^?)*
          funcs    (id^?)*
          tables   (id^?)*
          mems     (id^?)*
          globals  (id^?)*
          elem     (id^?)*
          data     (id^?)*
          locals   (id^?)*
          labels   (id^?)*
          typedefs (id^?)*

Note, that order matters. We are only concerned with the index. If an identifier is used, then we find the corresponding index of that identifier and put it in the abstract syntax tree
## Types
numtype --> 'i32' -> i32
            'i64' -> i64
            'f32' -> f32
            'f64' -> f64

vectype  --> 'v128' -> v128

reftype  --> 'funcref'   -> funcref
             'externref' -> externref

heaptype --> 'func'      -> funcref
             'extern'    -> externref

valtype  --> t:numtype -> t
             t:vectype -> t
             t:reftype -> t

Note: The optional identifier names for parameters in a function type only have documentation purpose. They cannot be referenced from anywhere.

functype --> '(' 'func' t_1*: vec(param) t_2*: vec(result) ')' -> [t_1*] -> [t_2*]

Note: multiple anonymous parameters or results may be combined into a single declaration:

param    --> '(' 'param' id^? t:valtype ')' -> t
result   --> '(' 'result' t:valtype ')'     -> t

'(' 'param' valtype* ')'  == ('(' 'param' valtype ')' )*
'(' 'result' valtype* ')' == ('(' 'result' valtype ')' )*

limits --> n:u32       -> {min n, max ε}
       --> n:u32 m:u32 -> {min n, max m}

memtype --> lim:limits -> lim

tabletype --> lim:limits et:reftype -> lim et

globaltype --> t:valtype -> const t
            |  '(' 'mut' t:valtype ')' -> var t

## Instructions
Structured control instructions can be annoated with a symbolic label identifier. They are only symbolic identifiers that can be bound **locally** in an instruction sequence. 
The following grammar handles the corresponding update to the identifier context by composing the context with an additional label entry:

label   -->  v:id -> {labels v} + I                        (if v not in I.labels)
         |   v:id -> {labels v} + I (I with labels[i] = ε) (if v in I.labels)
         |   ε    -> {labels v} + I

The new label entry is inserrted at the beginning of the label list in the identifier context. This shifts all existing labels up by one, mirroring the fact that control instructions are indexed relatively not absolutely.


## Modules
Type definitions can bind a symbolic type identifier:

type   -->   '(' 'type' id^? ft:functype ')'  -> ft


Type uses are **references** to type definitions
typeuse   --> '(' 'type' x:typeidx ')'                          -> x,I
                    (if I.typedefs[x] = [t^n_1] -> [t^*_2] and I = locals(ε)^n)

           |  '(' 'type' x:typeidx ')' (t1:param)* (t2:result)* -> x,I
                    (if I.typedefs[x] = [t^*_1] -> [t^*_2] and I = locals( id(param) )^*) well-formed

The synthesized attribute of a typeuse is a pair consisting of both the used type index and the local identifier context containing all possible parameter identifiers. **The following auxiliary function extracts optional identifiers from parameters:**
id('(' 'param' id^? ... ')')

The purpose of typeuses is to bind type definitions to an index or symbolic identifier. In this way it is a method to reference a type definition



Terminals: 
i32
i64
f32
f64

LOCALGET
LOCALSET