package edu.lehigh.cse262.slang.Interpreter;

import edu.lehigh.cse262.slang.Env.Env;
import edu.lehigh.cse262.slang.Parser.IAstVisitor;
import edu.lehigh.cse262.slang.Parser.IValue;
import edu.lehigh.cse262.slang.Parser.Nodes;

/**
 * ExprEvaluator evaluates an AST node. It is the heart of the evaluation
 * portion of our interpreter.
 */
public class ExprEvaluator implements IAstVisitor<IValue> {
    /** The environment in which to do the evaluation */
    private Env env;

    /** Construct an ExprEvaluator by providing an environment */
    public ExprEvaluator(Env env) {
        this.env = env;
    }

    /** Interpret an Identifier */
    @Override
    public IValue visitIdentifier(Nodes.Identifier expr) throws Exception {
        throw new Exception("visitIdentifier is not yet implemented");
    }

    /**
     * Interpret a Define special-form
     *
     * NB: it's OK for this to return null, because definitions aren't
     * expressions
     */
    @Override
    public IValue visitDefine(Nodes.Define expr) throws Exception {
        throw new Exception("visitDefine is not yet implemented");
    }

    /** Interpret a Bool value */
    @Override
    public IValue visitBool(Nodes.Bool expr) throws Exception {
        throw new Exception("visitBool is not yet implemented");
    }

    /** Interpret an Int value */
    @Override
    public IValue visitInt(Nodes.Int expr) throws Exception {
        throw new Exception("visitInt is not yet implemented");
    }

    /** Interpret a Dbl value */
    @Override
    public IValue visitDbl(Nodes.Dbl expr) throws Exception {
        throw new Exception("visitDbl is not yet implemented");
    }

    /** Interpret a Lambda value */
    @Override
    public IValue visitLambdaVal(Nodes.LambdaVal expr) throws Exception {
        throw new Exception("visitLambdaVal is not yet implemented");
    }

    /**
     * Interpret a Lambda definition by creating a Lambda value from it in the
     * current environment
     */
    @Override
    public IValue visitLambdaDef(Nodes.LambdaDef expr) throws Exception {
        throw new Exception("visitLambdaDef is not yet implemented");
    }

    /** Interpret an If expression */
    @Override
    public IValue visitIf(Nodes.If expr) throws Exception {
        throw new Exception("visitIf is not yet implemented");
    }

    /**
     * Interpret a set! special form. As with Define, this isn't an expression,
     * so it can return null
     */
    @Override
    public IValue visitSet(Nodes.Set expr) throws Exception {
        throw new Exception("visitSet is not yet implemented");
    }

    /** Interpret an And expression */
    @Override
    public IValue visitAnd(Nodes.And expr) throws Exception {
        throw new Exception("visitAnd is not yet implemented");
    }

    /** Interpret an Or expression */
    @Override
    public IValue visitOr(Nodes.Or expr) throws Exception {
        throw new Exception("visitOr is not yet implemented");
    }

    /** Interpret a Begin expression */
    @Override
    public IValue visitBegin(Nodes.Begin expr) throws Exception {
        throw new Exception("visitBegin is not yet implemented");
    }

    /** Interpret a "not special form" expression */
    @Override
    public IValue visitApply(Nodes.Apply expr) throws Exception {
        throw new Exception("visitApply is not yet implemented");
    }

    /** Interpret a Cons value */
    @Override
    public IValue visitCons(Nodes.Cons expr) throws Exception {
        throw new Exception("visitCons is not yet implemented");
    }

    /** Interpret a Vec value */
    @Override
    public IValue visitVec(Nodes.Vec expr) throws Exception {
        throw new Exception("visitVec is not yet implemented");
    }

    /** Interpret a Symbol value */
    @Override
    public IValue visitSymbol(Nodes.Symbol expr) throws Exception {
        throw new Exception("visitSymbol is not yet implemented");
    }

    /** Interpret a Quote expression */
    @Override
    public IValue visitQuote(Nodes.Quote expr) throws Exception {
        throw new Exception("visitQuote is not yet implemented");
    }

    /** Interpret a quoted datum expression */
    @Override
    public IValue visitTick(Nodes.Tick expr) throws Exception {
        throw new Exception("visitTick is not yet implemented");
    }

    /** Interpret a Char value */
    @Override
    public IValue visitChar(Nodes.Char expr) throws Exception {
        throw new Exception("visitChar is not yet implemented");
    }

    /** Interpret a Str value */
    @Override
    public IValue visitStr(Nodes.Str expr) throws Exception {
        throw new Exception("visitStr is not yet implemented");
    }

    /** Interpret a Built-In Function value */
    @Override
    public IValue visitBuiltInFunc(Nodes.BuiltInFunc expr) throws Exception {
        throw new Exception("visitBuiltInFunc is not yet implemented");
    }

    /** Interpret a Cons expression */
    @Override
    public IValue visitCond(Nodes.Cond expr) throws Exception {
        throw new Exception("visitCond is not yet implemented");
    }
}