# Regular Expressions for Scanning the CSE 262 Version of Scheme

Below there are six sub-sections, which correspond to the six .png files in this
folder.  Each section contains a mermaid.js script for drawing the corresponding
finite state machine.

These can be pasted into the mermaid live editor (<https://mermaid.live/edit>)
in order to modify them and interact with them.  There is also a VSCode plugin
for mermaid.js, but unfortunately it cannot handle comments or `style` syntax.
If you wish to visualize these diagrams in the Markdown Preview of VSCode, then
you'll need to delete the comments and the styles.

## Keywords

```mermaid
graph TD
    %% These aren't tokens, but they are real states
    START((START)) %% each time around the while loop, we start here

    %% These are the states that correspond to Scanner tokens.
    AND((AND))
    BEGIN((BEGIN))
    COND((COND))
    DEFINE((DEFINE))
    IF((IF))
    LAMBDA((LAMBDA))
    OR((OR))
    QUOTE((QUOTE))
    SET((SET))
    
    %% Transient and Non-Accepting States
    CLEANBREAK((CLEANBREAK))

    %% Rules

    START --"and"-->    AND
    START --"begin"-->  BEGIN
    START --"cond"-->   COND
    START --"define"--> DEFINE
    START --"if"-->     IF
    START --"lambda"--> LAMBDA
    START --"or"-->     OR
    START --"quote"-->  QUOTE
    START --"set!"-->   SET


    AND        --ε--> CLEANBREAK
    BEGIN      --ε--> CLEANBREAK
    COND       --ε--> CLEANBREAK
    DEFINE     --ε--> CLEANBREAK
    IF         --ε--> CLEANBREAK
    LAMBDA     --ε--> CLEANBREAK
    OR         --ε--> CLEANBREAK
    QUOTE      --ε--> CLEANBREAK
    SET        --ε--> CLEANBREAK

    %% Make sure all the tokens have a special color, to distinguish them
    style AND fill:#999999
    style BEGIN fill:#999999
    style COND fill:#999999
    style DEFINE fill:#999999
    style IF fill:#999999
    style LAMBDA fill:#999999
    style OR fill:#999999
    style QUOTE fill:#999999
    style SET fill:#999999
```

## Identifiers and Numbers

```mermaid
%% Identifiers and Numbers

graph TD
    %% These aren't tokens, but they are real states
    START((START)) %% each time around the while loop, we start here

    %% These are the states that correspond to Scanner tokens.
    IDENTIFIER((IDENTIFIER))
    DBL((DBL))
    INT((INT))
    
    %% Transient and Non-Accepting States
    ININT((ININT))
    INDBL((INDBL))
    PREDBL((PREDBL))
    CLEANBREAK((CLEANBREAK))
    PM((PM))
    INID((INID))

    %% Rules
    START --"{!$%&*/:<=>?~_^} or {a-z} or {A-Z}"--> INID

    INID --"{!$%&*/:<=>?~_^} or {0-9} or {a-z} or {A-Z} or {.+-}"--> INID
    INID --ε--> IDENTIFIER

    START --"{+, -}"--> PM
    PM --ε--> IDENTIFIER
    PM --"{0-9}"--> ININT

    START --"{0-9}"--> ININT
    ININT --"{0-9}"--> ININT
    ININT --ε--> INT
    ININT --"."--> PREDBL
    PREDBL --"{0-9}"--> INDBL
    INDBL --"{0-9}"--> INDBL
    INDBL --ε--> DBL

    INT        --ε--> CLEANBREAK
    DBL        --ε--> CLEANBREAK
    IDENTIFIER --ε--> CLEANBREAK

    %% Make sure all the tokens have a special color, to distinguish them
    style IDENTIFIER fill:#999999
    style DBL fill:#999999
    style INT fill:#999999
```

## Vector, Char, and Bool

```mermaid
%% Vectors, Chars, and Bools

graph TD
    %% These aren't tokens, but they are real states
    START((START)) %% each time around the while loop, we start here

    %% These are the states that correspond to Scanner tokens.
    VEC((VEC))
    BOOL((BOOL))
    CHAR((CHAR))
    
    %% Transient and Non-Accepting States
    VCB((VCB))
    PRECHAR((PRECHAR))
    CLEANBREAK((CLEANBREAK))

    %% Rules

    START --"#"--> VCB %% Vec or Char or Bool
    
    VCB --"("-->      VEC
    VCB --"{t, f}"--> BOOL
    VCB --"\"-->      PRECHAR

    VCB --"{'\newline', '\space', '\tab'}"--> CHAR
    
    PRECHAR --"any character not in {' ', '\t', '\n', '\r', '\0'}" -->CHAR

    BOOL       --ε--> CLEANBREAK
    CHAR       --ε--> CLEANBREAK

    VEC       --ε-->    START


    %% Make sure all the tokens have a special color, to distinguish them
    style VEC fill:#999999
    style BOOL fill:#999999
    style CHAR fill:#999999
```

## Special Symbols

```mermaid
%% Special Symbols

graph TD
    %% These aren't tokens, but they are real states
    START((START)) %% each time around the while loop, we start here

    %% These are the states that correspond to Scanner tokens.
    ABBREV((ABBREV))
    LPAREN((LPAREN))
    RPAREN((RPAREN))
    EOF((EOF))
    
    %% Transient and Non-Accepting States
    INCOMMENT((INCOMMENT))
    CLEANBREAK((CLEANBREAK))

    %% Rules
    START --"'"--> ABBREV
    START --ε-->   CLEANBREAK

    CLEANBREAK --"{' ', '\t', '\n', '\r'}"--> START

    CLEANBREAK --"("--> LPAREN
    CLEANBREAK --")"--> RPAREN
    CLEANBREAK --";"--> INCOMMENT

    INCOMMENT --"any character except \n or \0"--> INCOMMENT

    LPAREN    --ε-->    START
    RPAREN    --ε-->    START
    ABBREV    --ε-->    START
    INCOMMENT --"\n"--> START

    INCOMMENT  --"\0"--> EOF
    CLEANBREAK --"\0"--> EOF

    %% Make sure all the tokens have a special color, to distinguish them
    style LPAREN fill:#999999
    style RPAREN fill:#999999
    style ABBREV fill:#999999
    style EOF fill:#999999
```

## Strings

```mermaid
%% Strings

graph TD
    %% These aren't tokens, but they are real states
    START((START)) %% each time around the while loop, we start here

    %% These are the states that correspond to Scanner tokens.
    STR((STR))
    
    %% Transient and Non-Accepting States
    INSTR((INSTR))
    INSTR+((INSTR+))
    CLEANBREAK((CLEANBREAK))

    %% Rules

    START --"&quot;"--> INSTR
    INSTR --"any character not in {&quot;, \\, \n, \r, \t}"--> INSTR
    INSTR --'\'--> INSTR+
    INSTR+ --"{&quot;, \, t, n}"--> INSTR
    INSTR --"&quot;"--> STR

    STR        --ε--> CLEANBREAK

    %% Make sure all the tokens have a special color, to distinguish them
    style STR fill:#999999
```

## Full Diagram

```mermaid
graph TD
    %% These aren't tokens, but they are real states
    START((START)) %% each time around the while loop, we start here
    EOF((EOFTOKEN))

    %% These are the states that correspond to Scanner tokens.
    LPAREN((LPAREN))
    RPAREN((RPAREN))
    ABBREV((ABBREV))
    VEC((VEC))
    BOOL((BOOL))
    IDENTIFIER((IDENTIFIER))
    STR((STR))
    CHAR((CHAR))
    DBL((DBL))
    INT((INT))
    AND((AND))
    BEGIN((BEGIN))
    COND((COND))
    DEFINE((DEFINE))
    IF((IF))
    LAMBDA((LAMBDA))
    OR((OR))
    QUOTE((QUOTE))
    SET((SET))
    
    %% Transient and Non-Accepting States
    VCB((VCB))
    PRECHAR((PRECHAR))
    INCOMMENT((INCOMMENT))
    INSTR((INSTR))
    INSTR+((INSTR+))
    ININT((ININT))
    INDBL((INDBL))
    PREDBL((PREDBL))
    CLEANBREAK((CLEANBREAK))
    PM((PM))
    INID((INID))

    %% Rules
    START --"'"--> ABBREV
    START --ε-->   CLEANBREAK

    CLEANBREAK --"{' ', '\t', '\n', '\r'}"--> START

    CLEANBREAK --"("--> LPAREN
    CLEANBREAK --")"--> RPAREN
    CLEANBREAK --";"--> INCOMMENT

    START --"#"--> VCB %% Vec or Char or Bool
    
    VCB --"("-->      VEC
    VCB --"{t, f}"--> BOOL
    VCB --"\"-->      PRECHAR

    VCB --"{'\newline', '\space', '\tab'}"--> CHAR
    
    PRECHAR --"any character not in {' ', '\t', '\n', '\r', '\0'}" -->CHAR

    INCOMMENT --"any character except \n or \0"--> INCOMMENT

    START --"{!$%&*/:<=>?~_^} or {a-z} or {A-Z}"--> INID

    INID --"{!$%&*/:<=>?~_^} or {0-9} or {a-z} or {A-Z} or {.+-}"--> INID
    INID --ε--> IDENTIFIER

    START --"{+, -}"--> PM
    PM --ε--> IDENTIFIER
    PM --"{0-9}"--> ININT

    START --"{0-9}"--> ININT
    ININT --"{0-9}"--> ININT
    ININT --ε--> INT
    ININT --"."--> PREDBL
    PREDBL --"{0-9}"--> INDBL
    INDBL --"{0-9}"--> INDBL
    INDBL --ε--> DBL

    START --"and"-->    AND
    START --"begin"-->  BEGIN
    START --"cond"-->   COND
    START --"define"--> DEFINE
    START --"if"-->     IF
    START --"lambda"--> LAMBDA
    START --"or"-->     OR
    START --"quote"-->  QUOTE
    START --"set!"-->   SET

    START --"&quot;"--> INSTR
    INSTR --"any character not in {&quot;, \\, \n, \r, \t}"--> INSTR
    INSTR --'\'--> INSTR+
    INSTR+ --"{&quot;, \, t, n}"--> INSTR
    INSTR --"&quot;"--> STR

    INT        --ε--> CLEANBREAK
    DBL        --ε--> CLEANBREAK
    STR        --ε--> CLEANBREAK
    AND        --ε--> CLEANBREAK
    BEGIN      --ε--> CLEANBREAK
    COND       --ε--> CLEANBREAK
    DEFINE     --ε--> CLEANBREAK
    IF         --ε--> CLEANBREAK
    LAMBDA     --ε--> CLEANBREAK
    OR         --ε--> CLEANBREAK
    QUOTE      --ε--> CLEANBREAK
    SET        --ε--> CLEANBREAK
    IDENTIFIER --ε--> CLEANBREAK
    BOOL       --ε--> CLEANBREAK
    CHAR       --ε--> CLEANBREAK

    VEC       --ε-->    START
    LPAREN    --ε-->    START
    RPAREN    --ε-->    START
    ABBREV    --ε-->    START
    INCOMMENT --"\n"--> START

    INCOMMENT  --"\0"--> EOF
    CLEANBREAK --"\0"--> EOF

    %% Make sure all the tokens have a special color, to distinguish them
    style LPAREN fill:#999999
    style RPAREN fill:#999999
    style ABBREV fill:#999999
    style VEC fill:#999999
    style BOOL fill:#999999
    style IDENTIFIER fill:#999999
    style STR fill:#999999
    style CHAR fill:#999999
    style DBL fill:#999999
    style INT fill:#999999
    style AND fill:#999999
    style BEGIN fill:#999999
    style COND fill:#999999
    style DEFINE fill:#999999
    style IF fill:#999999
    style LAMBDA fill:#999999
    style OR fill:#999999
    style QUOTE fill:#999999
    style SET fill:#999999
    style EOF fill:#999999
```
