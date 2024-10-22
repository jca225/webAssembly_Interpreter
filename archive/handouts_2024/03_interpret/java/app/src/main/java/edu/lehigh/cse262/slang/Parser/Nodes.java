package edu.lehigh.cse262.slang.Parser;

import java.util.List;

import edu.lehigh.cse262.slang.Env.Env;

/**
 * Nodes is a wrapper class. Or, if you prefer, it is a hack to get a
 * "namespace" in Java.
 *
 * The high-level goal here is to set up 22 different classes, to represent the
 * 22 different nodes that can appear in our AST. Like in Tokens.java, we're
 * embedding them all in a wrapper class, so that there are fewer imports and
 * less overall code.
 * 
 * Unlike Tokens.java, these nodes are pretty diverse, and it is important for
 * students to understand what each is doing.
 *
 * If you don't like this kind of code, that's OK. It's ugly. It's a hack. It's
 * just organized like this so that we don't need 23 files of boilerplate code.
 * Better yet, you don't need to edit this file, so as long as you can
 * understand what's going on here, you're good.
 */
public class Nodes {
    /**
     * BaseNode is the base class for all of the nodes in our abstract syntax
     * tree. Even though BaseNode doesn't have any local fields, we define it as
     * an abstract class instead of an interface, so that the AST infrastructure
     * is symmetric with the Token infrastructure.
     */
    public static abstract class BaseNode {
        /**
         * Visit the AstNode to produce a String. This is useful for visitors
         * who want to print the AST for debugging.
         *
         * @param visitor The visitor object
         *
         * @return A string that was produced by the visitor
         */
        public abstract String visitString(IAstVisitor<String> visitor) throws Exception;

        /**
         * Visit the AstNode to produce a value (IValue). This is useful for
         * actually interpreting the program.
         *
         * @param visitor The visitor object
         *
         * @return A value that was produced by the visitor
         */
        public abstract IValue visitValue(IAstVisitor<IValue> visitor) throws Exception;
    }

    /** The `and` special form */
    public static class And extends BaseNode {
        /** The expressions to evaluate when computing `and` */
        public final List<BaseNode> expressions;

        /** Construct an `and` node from a list of expressions */
        public And(List<BaseNode> expressions) {
            this.expressions = expressions;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitAnd(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitAnd(this);
        }
    }

    /** The function apply form (the default form) */
    public static class Apply extends BaseNode {
        /** The set of expressions that comprise this apply */
        public final List<BaseNode> expressions;

        /** Construct an apply node from a list of expressions */
        public Apply(List<BaseNode> expressions) {
            this.expressions = expressions;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitApply(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitApply(this);
        }
    }

    /** The `begin` special form */
    public static class Begin extends BaseNode {
        /** The expressions to evaluate when computing `begin` */
        public final List<BaseNode> expressions;

        /** Construct a `begin` node from a list of expressions */
        public Begin(List<BaseNode> expressions) {
            this.expressions = expressions;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitBegin(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitBegin(this);
        }
    }

    /**
     * Bool is a boolean node: it is an AstNode that can be treated as a value
     */
    public static class Bool extends BaseNode implements IValue {
        /** The value represented by this node */
        public final boolean val;

        /** Construct a `bool` node from a boolean value */
        public Bool(boolean val) {
            this.val = val;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitBool(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitBool(this);
        }
    }

    /**
     * BuiltInFunc is a built-in function that can be executed. It is a
     * first-class value.
     */
    public static class BuiltInFunc extends BaseNode implements IValue {
        /** The name associated with this function. Useful for debugging */
        public final String name;

        /** The (Java) code to run to execute this function */
        public final IExecutable func;

        /**
         * Construct a `built in function` from a name and some executable Java
         * code
         */
        public BuiltInFunc(String name, IExecutable func) {
            this.name = name;
            this.func = func;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitBuiltInFunc(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitBuiltInFunc(this);
        }
    }

    /** Char is a character node: it is an AstNode that can be treated as a value */
    public static class Char extends BaseNode implements IValue {
        /** The value represented by this node */
        public final char val;

        /** Construct a `char` node from a character value */
        public Char(char val) {
            this.val = val;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitChar(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitChar(this);
        }
    }

    /** The `cond` special form */
    public static class Cond extends BaseNode {
        /** A Cond consists of a sequence of conditions, which we represent here */
        public static class Condition {
            /** The test */
            public BaseNode test;
            /** The expressions to evaluate if the condition is true */
            public List<BaseNode> expressions;

            /** Construct a condition from a test and set of expressions */
            public Condition(BaseNode test, List<BaseNode> expressions) {
                this.test = test;
                this.expressions = expressions;
            }
        }

        /** The set of conditions for this Cond */
        public List<Condition> conditions;

        /** Construct a `cond` from a set of expressions */
        public Cond(List<Condition> conditions) {
            this.conditions = conditions;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitCond(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitCond(this);
        }
    }

    /**
     * Cons is a pair (cons cell): it is an AstNode that can be treated as a
     * value
     */
    public static class Cons extends BaseNode implements IValue {
        /** The first value of the pair */
        public IValue car;

        /** The second value of the pair */
        public IValue cdr;

        /**
         * Construct a `cons` node from a list. This can produce a linked list
         * of Cons cells.
         */
        public Cons(List<IValue> items, Cons empty) throws Exception {
            if (items.size() == 0) {
                throw new Exception("Cannot construct Cons from empty list");
            } else if (items.size() == 1) {
                this.car = items.get(0);
                this.cdr = empty;
            } else {
                this.car = items.get(0);
                this.cdr = new Cons(items.subList(1, items.size()), empty);
            }
        }

        /**
         * Construct a `cons` node from two values. We can use this to make `pair`
         * cells.
         */
        public Cons(IValue car, IValue cdr) {
            this.car = car;
            this.cdr = cdr;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitCons(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitCons(this);
        }
    }

    /** Dbl is a double node: it is an AstNode that can be treated as a value */
    public static class Dbl extends BaseNode implements IValue {
        /** The value represented by this node */
        public final double val;

        /** Construct a `dbl` node from a double value */
        public Dbl(double val) {
            this.val = val;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitDbl(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitDbl(this);
        }
    }

    /** The `define` special form */
    public static class Define extends BaseNode {
        /** The identifier whose value is being defined */
        public final Identifier identifier;

        /** The expression to evaluate when deciding the value to define */
        public final BaseNode expression;

        /** Construct a `define` node from an identifier and expression */
        public Define(Identifier identifier, BaseNode expression) {
            this.identifier = identifier;
            this.expression = expression;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitDefine(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitDefine(this);
        }
    }

    /** Identifier represents a name (identifier) that can be bound to a value */
    public static class Identifier extends BaseNode {
        /** The name associated with this identifier */
        public final String name;

        /** Construct an `identifier` node from its name */
        public Identifier(String name) {
            this.name = name;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitIdentifier(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitIdentifier(this);
        }
    }

    /** The `if` special form */
    public static class If extends BaseNode {
        /** The expression to evaluate to true or false */
        public final BaseNode cond;

        /** The expression to evaluate if true */
        public final BaseNode ifTrue;

        /** The expression to evaluate if false */
        public final BaseNode ifFalse;

        /** Construct an `if` node from its test, true, and false expressions */
        public If(BaseNode cond, BaseNode ifTrue, BaseNode ifFalse) {
            this.cond = cond;
            this.ifTrue = ifTrue;
            this.ifFalse = ifFalse;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitIf(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitIf(this);
        }
    }

    /** Int is an integer node: it is an AstNode that can be treated as a value */
    public static class Int extends BaseNode implements IValue {
        /** The value represented by this node */
        public final int val;

        /** Construct an `int` node from an integer value */
        public Int(int val) {
            this.val = val;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitInt(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitInt(this);
        }
    }

    /** The `lambda` special form */
    public static class LambdaDef extends BaseNode {
        /** The identifiers that are the formal arguments to the function */
        public final List<Identifier> formals;

        /** The body of the function */
        public final List<BaseNode> body;

        /** Construct a `lambda` node from its formals and body */
        public LambdaDef(List<Identifier> formals, List<BaseNode> body) {
            this.formals = formals;
            this.body = body;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitLambdaDef(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitLambdaDef(this);
        }
    }

    /**
     * LambdaVal is the result of *evaluating* a Lambda expression. It is a
     * function that can be "executed". It is a first-class value.
     * 
     * [CSE 262] Note that the Parser cannot create LambdaVals... they're something
     * we get by *evaluating*.
     */
    public static class LambdaVal extends BaseNode implements IValue {
        /** The (static) scope at the time this LambdaVal was created */
        public final Env env;

        /** The lambda expression from which this LambdaVal was created */
        public final LambdaDef lambda;

        /**
         * Construct a `lambda value` from an environment and a definition of a
         * lambda
         */
        public LambdaVal(Env env, LambdaDef lambda) {
            this.env = env;
            this.lambda = lambda;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitLambdaVal(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitLambdaVal(this);
        }
    }

    /** The `or` special form */
    public static class Or extends BaseNode {
        /** The expressions to evaluate when computing `or` */
        public final List<BaseNode> expressions;

        /** Construct an `or` node from a list of expressions */
        public Or(List<BaseNode> expressions) {
            this.expressions = expressions;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitOr(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitOr(this);
        }
    }

    /** The `quote` special form' */
    public static class Quote extends BaseNode {
        /** The value that is being quoted */
        public final IValue datum;

        /** Construct a `quote` node from the datum being quoted */
        public Quote(IValue datum) {
            this.datum = datum;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitQuote(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitQuote(this);
        }
    }

    /** The `set!` special form */
    public static class Set extends BaseNode {
        /** The identifier whose value is being set */
        public final Identifier identifier;

        /** The expression to evaluate when deciding the value to set! */
        public final BaseNode expression;

        /** Construct a `set!` node from an identifier and expression */
        public Set(Identifier identifier, BaseNode expression) {
            this.identifier = identifier;
            this.expression = expression;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitSet(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitSet(this);
        }
    }

    /** Str is a string node: it is an AstNode that can be treated as a value */
    public static class Str extends BaseNode implements IValue {
        /** The value represented by this node */
        public final String val;

        /** Construct a `str` node from a String value */
        public Str(String val) {
            this.val = val;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitStr(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitStr(this);
        }
    }

    /**
     * Symbol represents a Scheme symbol: it is an AstNode that can be treated as a
     * value
     *
     * NB: Since Scheme is homo-iconic, Symbol and Identifier look identical.
     * However, a Symbol *is* a value, and an Identifier *is not*
     */
    public static class Symbol extends BaseNode implements IValue {
        /** The name associated with this symbol */
        public final String name;

        /** Construct a `symbol` node from its name */
        public Symbol(Object name) {
            this.name = (String) name;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitSymbol(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitSymbol(this);
        }
    }

    /** The `'` special form' */
    public static class Tick extends BaseNode {
        /** The value that is being quoted */
        public final IValue datum;

        /** Construct a `'` node from the datum being quoted */
        public Tick(IValue datum) {
            this.datum = datum;
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitTick(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitTick(this);
        }
    }

    /** Vec is a vector node: it is an AstNode that can be treated as a value */
    public static class Vec extends BaseNode implements IValue {
        /** The values represented by this node */
        public final IValue[] items;

        /** Construct a `vec` node from a list of values */
        public Vec(List<IValue> items) {
            IValue[] tmp = new IValue[items.size()];
            this.items = (IValue[]) items.toArray(tmp);
        }

        @Override
        public String visitString(IAstVisitor<String> visitor) throws Exception {
            return visitor.visitVec(this);
        }

        @Override
        public IValue visitValue(IAstVisitor<IValue> visitor) throws Exception {
            return visitor.visitVec(this);
        }
    }
}