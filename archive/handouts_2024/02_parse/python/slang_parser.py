import slang_scanner

# [CSE 262] You will probably find it tedious to create a whole class hierarchy
# for your Python parser.  Instead, consider whether each node type could just
# be a hash table.  In that case, you could have a function for "constructing"
# each "type", by putting some values into a hash table.


# A poor-man's enum: each of our token types is just a number
ABBREV, AND, BEGIN, BOOL, CHAR, COND, DBL, DEFINE, EOFTOKEN, IDENTIFIER, IF, INT, LAMBDA, LEFT_PAREN, OR, QUOTE, RIGHT_PAREN, SET, STR, VECTOR, DEF, BODY, FORMALS, LIST, APPLIC = range(
    0, 25)


TYPE = 'type'
VALUE = 'value'

class Parser:
    """The parser class is responsible for parsing a stream of tokens to produce
    an AST"""

    def __init__(self, true, false, empty):
        """Construct a parser by caching the environmental constants true,
        false, and empty"""
        self.true = true
        self.false = false
        self.empty = empty

    '''
    When we get to *interpretation*, we're going to want to avoid overheads for doing comparisons.  
    So rather than have lots and lots of objects that all are the boolean "true", or boolean "false", or the empty list, 
    we have three constants, and we'll make sure that every time we ever need a true or false or empty list, we use the constants, 
    instead of making new ones that are expensive to compare.
     - Prof. Spear
    '''
    def parse(self, tokens):

        expressions = [] # we append values to an empty list within a dictionary to account for more than one value

        while (tokens.nextToken().type != EOFTOKEN): # we check to make sure the current token we are on is not EOF
            
            # <definition> --> LPAREN DEFINE IDENTIFIER <expression> RPAREN
            if tokens.nextToken().type == LEFT_PAREN and tokens.nextNextToken().type == DEFINE: # definition
                # Pop previous two transient states LPAREN and DEFINE
                tokens.popToken()
                tokens.popToken() 
                expressions.append(self.definition(tokens))
            
            # Expression
            else: 
                expressions.append(self.expression(tokens))
            
        return expressions
    
    '''
    NOTE: All of these methods maintain the following invariant: upon each enter into the subroutine, the tokens.nextToken() is on
          the next token that must be parsed for that specific node. Furthermore, upon each exit of the subroutine, tokens.nexToken()
          is on the **next token that must be parsed for the next node.**
          Also note that all parentheses are transient: That is, we do not need any information about them once we are done traversing them in our token list
    '''
    def expression(self, tokens, grammar=None):
        
        # subgrammar type we will return
        sub_grammar = {}
        
        # <constant> --> BOOL | INT | DBL | CHAR | STR
        constant = self.constant(tokens)
        if constant != {}: 
            # we do not pop here because there are no transient states
            sub_grammar = constant
        
        # ABBREV <datum>
        # ABBREV is a short-hand for quote, and it is not able to be evaluated
        elif tokens.nextToken().type == ABBREV:
            tokens.popToken() # pop transient ABBREV
            sub_grammar[TYPE] = QUOTE
            sub_grammar[VALUE] = self.datum(tokens)
        
        elif tokens.nextToken().type == LEFT_PAREN:
            tokens.popToken() # LPAREN is transient
            # LPAREN QUOTE <datum> RPAREN
            if tokens.nextToken().type == QUOTE:
                tokens.popToken() # QUOTE is transient
                sub_grammar[TYPE] = QUOTE
                sub_grammar[VALUE] = self.datum(tokens)

            # LPAREN LAMBDA <formals> <body> RPAREN
            # Note that lambdas do require environments
            elif tokens.nextToken().type == LAMBDA: 
                tokens.popToken() # LAMBDA is transient
                sub_grammar[TYPE] = LAMBDA
                formals = self.formals(tokens)
                body = self.body(tokens)
                sub_grammar[VALUE] = self.construct_lambda(formals, body)
        
            # LPAREN IF <expression> <expression> <expression> RPAREN
            elif tokens.nextToken().type == IF: 
                tokens.popToken() # IF is transient
                sub_grammar[TYPE] = IF
                for i in range(0,3):
                    sub_grammar[VALUE].append(self.expression(tokens))
                
            # LPAREN SET IDENTIFIER <expression> RPAREN    
            elif tokens.nextToken().type == SET:
                tokens.popToken() # pop transient 'SET'
                sub_grammar[TYPE] = SET
                sub_grammar[VALUE] = {IDENTIFIER: tokens.nextToken().tokenText()}
                tokens.popToken() # pop transient identifier
                sub_grammar[VALUE][VALUE] = self.expression(tokens)

            # LPAREN AND <expression>+ RPAREN
            elif tokens.nextToken().type == AND:
                tokens.popToken() # pop transient 'AND'
                sub_grammar[TYPE] = AND
                sub_grammar[VALUE] = []
                while tokens.nextToken().type != EOFTOKEN and tokens.nextToken().type != RIGHT_PAREN:
                    sub_grammar[VALUE].append(self.expression(tokens))
                
            # LPAREN OR <expression>+ RPAREN
            elif tokens.nextToken().type == OR:
                tokens.popToken() # pop transient 'OR'
                sub_grammar[TYPE] = OR
                sub_grammar[VALUE] = []
                while tokens.nextToken().type != EOFTOKEN and tokens.nextToken().type != RIGHT_PAREN:
                    sub_grammar[VALUE].append(self.expression(tokens))
                
            # LPAREN BEGIN <expression>+ RPAREN
            elif tokens.nextToken().type == BEGIN:
                tokens.popToken() # pop transient 'BEGIN'
                sub_grammar[TYPE] = BEGIN
                sub_grammar[VALUE] = []
                while tokens.nextToken().type != EOFTOKEN and tokens.nextToken().type != RIGHT_PAREN:
                    sub_grammar[VALUE].append(self.expression(tokens))
                
            # LPAREN COND <condition>+ RPAREN
            elif tokens.nextToken().type == COND:
                tokens.popToken() # pop transient 'COND'
                sub_grammar[TYPE] = COND
                sub_grammar[VALUE] = []
                while tokens.nextToken().type != EOFTOKEN and tokens.nextToken().type != RIGHT_PAREN: 
                    sub_grammar[VALUE].append(self.condition(tokens))
            # <application> --> LPAREN <expression>+ RPAREN
            else:
                sub_grammar[TYPE] = APPLIC
                sub_grammar[VALUE] = []
                while tokens.nextToken().type != EOFTOKEN and tokens.nextToken().type != RIGHT_PAREN:
                    sub_grammar[VALUE].append(self.expression(tokens))
                    
            # Check for and pop transient 'RPAREN'
            if tokens.nextToken().type != RIGHT_PAREN: # EOF consumed before Right parentheses
                raise Exception("There is no closing parentheses for token: " + tokens.nextToken().line)
            # pop transient RPAREN
            tokens.popToken() 

        # IDENTIFIER 
        else:
            sub_grammar = {TYPE: IDENTIFIER, VALUE: tokens.nextToken().tokenText}
            tokens.popToken() # pop identifier
        
        return sub_grammar

    # <definition> --> LPAREN DEFINE IDENTIFIER <expression> RPAREN
    def definition(self, tokens, grammar=None):
        sub_grammar = {}
        sub_grammar[TYPE] = DEF
        
        sub_grammar[VALUE] = {}
        sub_grammar[VALUE][IDENTIFIER] = tokens.nextToken().type
        
        tokens.popToken() # move from identifier to beginning of <expression>
        sub_grammar[VALUE][VALUE] = self.expression(tokens)

        if tokens.nextToken().type == EOFTOKEN: # EOF consumed before Right parentheses
            raise Exception("There is no closing parentheses for token: " + tokens.nextToken().line)
            
        tokens.popToken() # pop transient 'RPAREN'

        return sub_grammar

    # <datum> --> BOOL | INT | DBL | CHAR | STR | <symbol>  | <list>  | <vector>
    def datum(self, tokens):
                
        # BOOL | INT | DBL | CHAR | STR 
        constant = self.constant(tokens)
        if constant != {}:
            return constant
        
        # <symbol> --> IDENTIFIER
        elif tokens.nextToken().type == IDENTIFIER: # parse the identifier
            return_value = {TYPE: IDENTIFIER, VALUE: tokens.nextToken().literal} 
            tokens.popToken()
        
        # <vector>
        elif tokens.nextToken().type == VECTOR:
            return_value[TYPE] =  VECTOR
            return_value[VALUE] = []
            tokens.popToken() # Preserve the invariant!
            while tokens.nextToken().type != RIGHT_PAREN and tokens.nextToken().type != EOFTOKEN:
                return_value[VALUE].append(self.datum(tokens)) 
            if tokens.nextToken().type == EOFTOKEN: # EOF consumed before Right parentheses
                raise Exception("There is no closing parentheses for token: " + tokens.nextToken().line)
            tokens.popToken()
        
        # <list>
        elif tokens.nextToken().type == LEFT_PAREN: # list; identical to vector in parsing except for type
            return_value[TYPE] = 'list'
            return_value[VALUE] = []
            tokens.popToken()
            while tokens.nextToken().type != RIGHT_PAREN and tokens.nextToken().type != EOFTOKEN:
                return_value[VALUE].append(self.datum(tokens)) 
            if tokens.nextToken().type == EOFTOKEN: # EOF consumed before Right parentheses
                raise Exception("There is no closing parentheses for token: " + tokens.nextToken().line)
            tokens.popToken()
        return return_value
    

    # <formals> --> LPAREN IDENTIFIER* RPAREN
    def formals(self, tokens):
        grammar = {}
        grammar[TYPE] = FORMALS
        grammar[VALUE] = []
        # formal must have a left parentheses here
        if tokens.nextToken().type != LEFT_PAREN:
            raise Exception("There is no opening parentheses for token: " + tokens.nextToken().line)
        tokens.popToken() # increment stack to account for LPAREN
        
        # parse as many identifiers as needed
        while tokens.nextToken().type != EOFTOKEN and tokens.nextToken() != RIGHT_PAREN:
            if tokens.nextToken().type == IDENTIFIER: # parse the identifier
                grammar['value'].append({'type': 'identifier', 'value': tokens.nextToken().literal})
            else:
                raise Exception("Incorrect type. Expected token identifier on line: " + tokens.nextToken().line)
            tokens.popToken() # pop token from the stack
        
        if tokens.nextToken().type == EOFTOKEN: # EOF consumed before Right parentheses
            raise Exception("There is no closing parentheses for token: " + tokens.nextToken().line)
        return grammar


    # <body> --> <definition>* <expression>
    def body(self, tokens):
        grammar = {}
        grammar[TYPE] = BODY
        grammar[VALUE] = []
        while tokens.nextToken().type != EOFTOKEN and tokens.nextToken().type != RIGHT_PAREN:
            # <definition> --> LPAREN DEFINE IDENTIFIER <expression> RPAREN
            if tokens.nextToken().type == LEFT_PAREN and tokens.nextNextToken().type == DEFINE: # definition
                grammar[VALUE].append(self.definition(tokens))
            
            # Expression
            else: 
                grammar[VALUE].append(self.expression(tokens))
                break
            
            # Once we are done parsing the expression/definition, we need to make sure the next token is a closing parentheses:
            if tokens.nextToken().type != RIGHT_PAREN:
                 raise Exception("There is no closing parentheses for token: " + str(tokens.nextToken().line))
            # pop the token
            tokens.popToken()
        return grammar
        
    
    # <condition> --> LPAREN <expression> <expression>* RPAREN
    def condition(self, tokens):
        sub_grammar = {}
        sub_grammar[TYPE] = COND
        sub_grammar[VALUE] = []
        if tokens.nextToken().type == LEFT_PAREN:
            tokens.popToken()
            sub_grammar[VALUE].append(self.expression(tokens))
            while tokens.nextToken().type != RIGHT_PAREN and tokens.nextToken().type != EOFTOKEN:
                sub_grammar[VALUE].append(self.expression(tokens))
            
            # Once we are done parsing the expression/definition, we need to make sure the next token is a closing parentheses:
            if tokens.nextToken().type != RIGHT_PAREN:
                 raise Exception("There is no closing parentheses for token: " + str(tokens.nextToken().line))
            tokens.popToken()
        return sub_grammar
    
    def constant(self, tokens):
        '''
        The purpose of this function is to parse all of our constant values. In a sense it is all of the leaves
        of our Abstract Syntax Tree, the states that are recurrent (whatever way you would like to think about them).
        The point is this is a **recurrent function.**

        parameters:
        - tokens: instantiation of a wrapper class around a token list for better utilization
        returns:
        - a 'struct' in some sense, represented as a dictionary containing a type and a value field
        '''
        
        return_value = {}
        
        # the control flow in this method is very simple: we just check for the recurrent (==primitive) states
        if tokens.nextToken().type == BOOL:
            return_value = self.true if tokens.nextToken().tokenText == 'true' else self.false
        elif tokens.nextToken().type == INT:
            return_value = {TYPE: INT, VALUE: int(tokens.nextToken().literal)}
        elif tokens.nextToken().type == DBL:
            return_value = {TYPE: DBL, VALUE: float(tokens.nextToken().literal)}
        elif tokens.nextToken().type == CHAR:
            return_value = {TYPE: CHAR, VALUE: tokens.nextToken().literal}
        elif tokens.nextToken().type == STR:   
            return_value = {TYPE: STR, VALUE: tokens.nextToken().literal}  
        else:
            return {}
        tokens.popToken() # we are done with this token
        return return_value


'''

So we may need to add some more,
Some better method for constructing the XML 
eXtensible Markup Language
all XML is, is information wrapped in tags
It is designed as a method to carry data
almost like, units of measurement:
<feet>500</feet>
<yards>194</yards>

<feet-text>five-hundred</feet-text>

So you see, it is simply a method for defining data in a reasonable manner. 
Data that is sequential, and not in a table necessarily.

(QUOTE "hello")

Also note that with respect to the popTokens, there must be an invariant that is satisfied upon each enter of the function!!!
What should this invariant be.
We are on the current token that must be parsed



"
Also, regarding the environment... It's where local variables go.  
But since this is a language that supports first-class functions and closures, we can't just have a stack for call frames.  
Instead, we have a "cactus stack" (like a tree) that tracks the static scope of still-live closures.  
It'll make more sense when you get to part 4.

Call Stack is all the local variables within a subroutine

first-class functions are functions that are treated like any other variable. They may be inputted into functions, be returned,
or be saved in variables.
Languages with first-class functions treat a function as if they were variables. 
Higher-order functions are just a function returning a function, or that takes a function as an argument.

Closures are used to preserve outer scope inside an inner scope. This is useful to not clutter the global scope with variables and also to make variables act like they are private.

Closures take this a step further by allowing functions to remember variables from their containing scope.


"
--------------------------------------------------------------------------------------------------------------------------------------------------

how do we deal with the issue of tail-recursion -- that is, we may need to add them add the same time in the same level for things with *
this may also simplify the implementation
The specifics are a tad complicated, and will need to be further developed (more specifically what it is i am trying to do):

# non-tail recursion:
def fact(x) {
    if (x === 1) {
        return 1;
    } else {
        return x * recsum(x - 1);
    }
}

# tail-recursion
def factorial_tail(n, acc=1):
    if n == 0:
        return acc
    else:
        return factorial_tail(n - 1, n * acc)


okay so now how can we implement the tail recursion? And make this fit into our architecture?
Can this simplify our architecture on all possible levels?
Lets edit the architecture, it may be necessary to turn tokens into a global variable just for more ease of use, and see what happens;
I am confident an idea will arise.


web assembly will require an intermediate representation
what to do in code generation
first step to ir
IR - intermediate representation 
a = 1 + 2 + 3

a = 1 + 2
b = a + 3
every expression has two inputs rather than an arbitrary amount.
changing representation from one form to another

front end and backend exist -- the peak is where this is
pass in an AST to something more complicated -- the engine inside a compiler
popular: LLVM - compiler backend to rust, C++, swift
highly finely tuned
optimize in this area
CLANG is an alternative backend to gcc and CLANG uses LLVM for its inner workings
AST is the interface
At that point it does not care where the AST comes from 

Web assembly is another one of these engines, it is like a virtual machine that executes this web assembly byte code

A browser is a giant interpreter -- takes in programs it downloads from the internet and turns them and displays them
as graphically layed out shapes and things
programs that we write in c and java is we generate number of a web server or sort some lists
all of this test is colored and layed out and organized to some website
HTML is a lot like lisp -- a giant tree with a bunch of names
html -- relationships between everything
css -- what do these things look like
js -- behavior -- what happens after you click on something what happens exactly
three backends that must exist: js, css, and html

for a very long time you could only execute js
scripting engine with not a lot of features , then when the web started taking off java
started getting more capable and people required more modules, type systems, more robust
they now write javascript engines, shipped with many browsers

not everyone wants to write javascript, it still very lacking
this is where web assembly comes in, it is its own way of interfacing with the engine that can run javascript programs
but in a way that allows you to compile different languages to that backend
this means we need to put up with javascript limitations.
it is sandboxed -- restricted from using a lot of different computing resources.
Peripherals, gpus, the filesystem
threading
js programs are all single-threaded
they can achieve asynchrony, and maybe some parallelism is run outside of a browser.
Web gpu is a standard so you can access a gpu hardware via the browser
egui.rs, written in rust, it uses a lot of cpu and gpu

get resources back somehow via the web assembly backend





-------------------------------------------------------------------------------------------------------------------------------------------------

package edu.lehigh.cse262.slang.Parser;

/**
 * AstToXml is a visitor that produces, for each AST node, a string
 * representation of that node as XML. Note that this is not the same as an XML
 * file.
 * 
 * The escaping rules for AstToXml are the same as for TokenToXml.
 *
 * [CSE 262] Unlike TokenToXml, this file does nest some tags inside of other
 * tags. This should not be a surprise, since we are dealing with a
 * context-free grammar now, not a regular grammar.
 */
public class AstToXml implements IAstVisitor<String> {
    private int indentation = 0;

    private static String escape(String s) {
        var escaped = s.replace("\\", "\\\\").replace("\t", "\\t")
                .replace("\n", "\\n").replace("'", "\\'");
        return escaped;
    }

    private void indent(StringBuilder sb) {
        for (int i = 0; i < indentation; ++i)
            sb.append(" ");
    }

    @Override
    public String visitIdentifier(Nodes.Identifier expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Identifier val='" + escape(expr.name) + "' />\n");
        return sb.toString();
    }

    @Override
    public String visitDefine(Nodes.Define expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Define>\n");
        indentation++;
        sb.append(expr.identifier.visitString(this));
        sb.append(expr.expression.visitString(this));
        sb.append("</Define>\n");
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitBool(Nodes.Bool expr) {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Bool val='" + (expr.val ? "true" : "false") + "' />\n");
        return sb.toString();
    }

    @Override
    public String visitInt(Nodes.Int expr) {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Int val='" + expr.val + "' />\n");
        return sb.toString();
    }

    @Override
    public String visitDbl(Nodes.Dbl expr) {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Dbl val='" + expr.val + "' />\n");
        return sb.toString();
    }

    @Override
    public String visitLambdaDef(Nodes.LambdaDef expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Lambda>\n");
        indentation++;
        indent(sb);
        sb.append("<Formals>\n");
        indentation++;
        for (var f : expr.formals)
            sb.append(f.visitString(this));
        indentation--;
        indent(sb);
        sb.append("</Formals>\n");
        indent(sb);
        sb.append("<Expressions>\n");
        indentation++;
        for (var e : expr.body)
            sb.append(e.visitString(this));
        indentation--;
        indent(sb);
        sb.append("</Expressions>\n");
        indentation--;
        indent(sb);
        sb.append("</Lambda>\n");
        return sb.toString();
    }

    @Override
    public String visitIf(Nodes.If expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<If>\n");
        indentation++;
        sb.append(expr.cond.visitString(this));
        sb.append(expr.ifTrue.visitString(this));
        sb.append(expr.ifFalse.visitString(this));
        indentation--;
        indent(sb);
        sb.append("</If>\n");
        return sb.toString();
    }

    @Override
    public String visitSet(Nodes.Set expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Set>\n");
        indentation++;
        sb.append(expr.identifier.visitString(this));
        sb.append(expr.expression.visitString(this));
        indentation--;
        indent(sb);
        sb.append("</Set>\n");
        return sb.toString();
    }

    @Override
    public String visitAnd(Nodes.And expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<And>\n");
        indentation++;
        for (var e : expr.expressions)
            sb.append(e.visitString(this));
        indentation--;
        sb.append("</And>\n");
        return sb.toString();
    }

    @Override
    public String visitOr(Nodes.Or expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Or>\n");
        indentation++;
        for (var e : expr.expressions)
            sb.append(e.visitString(this));
        indentation--;
        sb.append("</Or>\n");
        return sb.toString();
    }

    @Override
    public String visitBegin(Nodes.Begin expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Begin>\n");
        indentation++;
        for (var e : expr.expressions)
            sb.append(e.visitString(this));
        indentation--;
        indent(sb);
        sb.append("</Begin>\n");
        return sb.toString();
    }

    @Override
    public String visitApply(Nodes.Apply expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Apply>\n");
        indentation++;
        for (var e : expr.expressions)
            sb.append(e.visitString(this));
        indentation--;
        indent(sb);
        sb.append("</Apply>\n");
        return sb.toString();
    }

    @Override
    public String visitCons(Nodes.Cons expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Cons>\n");
        indentation++;
        if (expr.car != null)
            sb.append(((Nodes.BaseNode) expr.car).visitString(this));
        else {
            indent(sb);
            sb.append("<Null />\n");
        }
        if (expr.cdr != null)
            sb.append(((Nodes.BaseNode) expr.cdr).visitString(this) + "\n");
        else {
            indent(sb);
            sb.append("<Null />\n");
        }
        indentation--;
        indent(sb);
        sb.append("</Cons>\n");
        return sb.toString();
    }

    @Override
    public String visitVec(Nodes.Vec expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Vector>\n");
        indentation++;
        for (var i : expr.items)
            sb.append(((Nodes.BaseNode) i).visitString(this));
        indentation--;
        sb.append("</Vector>\n");
        return null;
    }

    @Override
    public String visitSymbol(Nodes.Symbol expr) throws Exception {
        throw new Exception("Symbol should not be visited during AST printing");
    }

    @Override
    public String visitQuote(Nodes.Quote expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Quote>\n");
        indentation++;
        sb.append(((Nodes.BaseNode) expr.datum).visitString(this));
        indentation--;
        sb.append("</Quote>\n");
        return sb.toString();
    }

    @Override
    public String visitTick(Nodes.Tick expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Tick>\n");
        indentation++;
        sb.append(((Nodes.BaseNode) expr.datum).visitString(this));
        indentation--;
        sb.append("</Tick>\n");
        return sb.toString();
    }

    @Override
    public String visitChar(Nodes.Char expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Char val='" + escape("" + expr.val) + "' />\n");
        return sb.toString();
    }

    @Override
    public String visitStr(Nodes.Str expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Str val='" + escape(expr.val) + "' />\n");
        return sb.toString();
    }

    @Override
    public String visitBuiltInFunc(Nodes.BuiltInFunc expr) throws Exception {
        throw new Exception("BuiltInFunc should not be visited during AST printing");
    }

    @Override
    public String visitLambdaVal(Nodes.LambdaVal val) throws Exception {
        throw new Exception("LambdaVal should not be visited during AST printing");
    }

    @Override
    public String visitCond(Nodes.Cond expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("<Cond>\n");
        indentation++;
        for (var cond : expr.conditions) {
            indent(sb);
            sb.append("<Condition>\n");
            indentation++;
            indent(sb);
            sb.append("<Test>\n");
            indentation++;
            sb.append(cond.test.visitString(this));
            indentation--;
            indent(sb);
            sb.append("</Test>\n");
            indent(sb);
            sb.append("<Actions>\n");
            indentation++;
            for (var e : cond.expressions)
                sb.append(e.visitString(this));
            indentation--;
            indent(sb);
            sb.append("</Actions>\n");
            indentation--;
            indent(sb);
            sb.append("</Condition>\n");
        }
        indentation--;
        indent(sb);
        sb.append("</Cond>\n");
        return sb.toString();
    }
}
'''