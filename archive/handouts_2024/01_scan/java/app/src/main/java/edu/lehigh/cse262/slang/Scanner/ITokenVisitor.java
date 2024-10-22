package edu.lehigh.cse262.slang.Scanner;

/**
 * ITokenVisitor is a visitor over all of the token types. The visitor pattern
 * in this code is slightly degenerate, because Tokens are POJOs with only
 * public final fields. Thus we don't really need the responding calls from
 * Tokens to pass copies of their fields to the visitor... we can just give the
 * token itself, and then the visitor can read the final fields.
 *
 * [CSE 262] Given how straightforward and uniform the methods of this interface
 * are, there isn't much point in commenting them. If you understand the visitor
 * pattern, then you should understand this interface.
 */
public interface ITokenVisitor<T> {
    public T visitAbbrev(Tokens.Abbrev tok);

    public T visitAnd(Tokens.And tok);

    public T visitBegin(Tokens.Begin tok);

    public T visitBool(Tokens.Bool tok);

    public T visitChar(Tokens.Char tok);

    public T visitCond(Tokens.Cond tok);

    public T visitDbl(Tokens.Dbl tok);

    public T visitDefine(Tokens.Define tok);

    public T visitEof(Tokens.Eof tok);

    public T visitIdentifier(Tokens.Identifier tok);

    public T visitIf(Tokens.If tok);

    public T visitInt(Tokens.Int tok);

    public T visitLambda(Tokens.Lambda tok);

    public T visitLParen(Tokens.LeftParen tok);

    public T visitOr(Tokens.Or tok);

    public T visitQuote(Tokens.Quote tok);

    public T visitRParen(Tokens.RightParen tok);

    public T visitSet(Tokens.Set tok);

    public T visitStr(Tokens.Str tok);

    public T visitVector(Tokens.Vec tok);

    public T visitError(Tokens.Error tok);
}