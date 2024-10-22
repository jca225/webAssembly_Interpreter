package edu.lehigh.cse262.slang.Parser;

/**
 * IAstVisitor is a visitor over all of the AST Node types. As with
 * ITokenVisitor, we're visiting over POJOs with final fields (except Cons), so
 * we're just going to rebound and pass the objects back to the appropriate
 * methods of the visitor.
 *
 * NB: As in ITokenVisitor, there's not really any point in documenting these
 * methods.
 */
public interface IAstVisitor<T> {
    public T visitAnd(Nodes.And expr) throws Exception;

    public T visitApply(Nodes.Apply expr) throws Exception;

    public T visitBegin(Nodes.Begin expr) throws Exception;

    public T visitBool(Nodes.Bool expr) throws Exception;

    public T visitBuiltInFunc(Nodes.BuiltInFunc expr) throws Exception;

    public T visitChar(Nodes.Char expr) throws Exception;

    public T visitCons(Nodes.Cons expr) throws Exception;

    public T visitDefine(Nodes.Define expr) throws Exception;

    public T visitIdentifier(Nodes.Identifier expr) throws Exception;

    public T visitIf(Nodes.If expr) throws Exception;

    public T visitLambdaDef(Nodes.LambdaDef expr) throws Exception;

    public T visitLambdaVal(Nodes.LambdaVal expr) throws Exception;

    public T visitInt(Nodes.Int expr) throws Exception;

    public T visitDbl(Nodes.Dbl expr) throws Exception;

    public T visitOr(Nodes.Or expr) throws Exception;

    public T visitQuote(Nodes.Quote expr) throws Exception;

    public T visitSet(Nodes.Set expr) throws Exception;

    public T visitStr(Nodes.Str expr) throws Exception;

    public T visitSymbol(Nodes.Symbol expr) throws Exception;

    public T visitTick(Nodes.Tick expr) throws Exception;

    public T visitVec(Nodes.Vec expr) throws Exception;

    public T visitCond(Nodes.Cond expr) throws Exception;
}