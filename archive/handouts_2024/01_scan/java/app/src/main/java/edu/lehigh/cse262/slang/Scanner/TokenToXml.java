package edu.lehigh.cse262.slang.Scanner;

/**
 * TokenToXml is a visitor that produces, for each Token, a string
 * representation of that Token in XML. Note that this is not the same as an XML
 * file.
 *
 * [CSE 262] In lieu of documenting each method with a perfunctory comment, this
 * comment will document the entire TokenToXml behavior.
 *
 * [CSE 262] Every token will be printed as an XML entity. These entities will
 * have the form `<XyzToken />`. That is, tokens will not have a separate
 * `</XyzToken>` closing tag.
 *
 * [CSE 262] Except for EofToken, each XML entity will have `line` and `col`
 * attributes, to represent the line number where the token appears in the
 * source file, and the column index within the line. Column indexes are
 * 0-based. Line numbers are 1-based.
 *
 * [CSE 262] For tokens that have a literal (bool, char, double, int, string),
 * that literal will be an attribute of the XML entity called `val`. Unlike the
 * line and column, literals must be in single quotes, even if they are numbers.
 * We will treat IdentifierToken as if it has a literal.
 *
 * [CSE 262] The BoolToken should use the text `true` or `false`.
 *
 * [CSE 262] The CharToken, Identifier, and StrToken need to escape their values
 * as follows:
 * - tab should get the val '\t'
 * - newline should get the val '\n'
 * - `'` should get the val '\''
 * - `\` should get the val '\\`
 *
 * [CSE 262] Each XML entity should appear on a single line. There should not be
 * extra lines in the file. There should not be extra whitespace before or
 * after an entity.
 *
 * [CSE 262] Please keep in mind that the primary purpose of this XML-based
 * format is to make it easier for students to get full marks on later phases of
 * the assignment without completing earlier phases. A real compiler with XML
 * output of intermediate forms would need to be a fair bit more intelligent.
 */
public class TokenToXml implements ITokenVisitor<String> {
    /**
     * basicToken handles printing a token name, line, and column for simple
     * tokens
     */
    private static String basicToken(String name, Tokens.BaseToken tok) {
        return "<" + name + " line=" + tok.line + " col=" + tok.col + " />";
    }

    /**
     * escape() handles escaping a String, according to the discussion above
     *
     * Note that `escape` is intentionally a little bit broken. When you really
     * understand regular expressions, you'll understand what's wrong. When you
     * really understand scanning, you'll understand how to fix it. But you
     * don't have to fix it unless you want to :)
     */
    private static String escape(String s) {
        var escaped = s
                .replace("\\", "\\\\")
                .replace("\t", "\\t")
                .replace("\n", "\\n")
                .replace("'", "\\'");
        return escaped;
    }

    @Override
    public String visitAbbrev(Tokens.Abbrev tok) {
        return basicToken("AbbrevToken", tok);
    }

    @Override
    public String visitAnd(Tokens.And tok) {
        return basicToken("AndToken", tok);
    }

    @Override
    public String visitBegin(Tokens.Begin tok) {
        return basicToken("BeginToken", tok);
    }

    @Override
    public String visitBool(Tokens.Bool tok) {
        return "<BoolToken line=" + tok.line + " col=" + tok.col + " val='" + (tok.literal ? "true" : "false")
                + "' />";
    }

    @Override
    public String visitChar(Tokens.Char tok) {
        String lit = "" + tok.literal;
        return "<CharToken line=" + tok.line + " col=" + tok.col + " val='" + escape(lit) + "' />";
    }

    @Override
    public String visitCond(Tokens.Cond tok) {
        return basicToken("CondToken", tok);
    }

    @Override
    public String visitDbl(Tokens.Dbl tok) {
        return "<DblToken line=" + tok.line + " col=" + tok.col + " val='" + tok.literal + "' />";
    }

    @Override
    public String visitDefine(Tokens.Define tok) {
        return basicToken("DefineToken", tok);
    }

    @Override
    public String visitEof(Tokens.Eof tok) {
        return "<EofToken />";
    }

    @Override
    public String visitIdentifier(Tokens.Identifier tok) {
        return "<IdentifierToken line=" + tok.line + " col=" + tok.col + " val='" + escape(tok.tokenText) + "' />";
    }

    @Override
    public String visitIf(Tokens.If tok) {
        return basicToken("IfToken", tok);
    }

    @Override
    public String visitInt(Tokens.Int tok) {
        return "<IntToken line=" + tok.line + " col=" + tok.col + " val='" + tok.literal + "' />";
    }

    @Override
    public String visitLambda(Tokens.Lambda tok) {
        return basicToken("LambdaToken", tok);
    }

    @Override
    public String visitLParen(Tokens.LeftParen tok) {
        return basicToken("LParenToken", tok);
    }

    @Override
    public String visitOr(Tokens.Or tok) {
        return basicToken("OrToken", tok);
    }

    @Override
    public String visitQuote(Tokens.Quote tok) {
        return basicToken("QuoteToken", tok);
    }

    @Override
    public String visitRParen(Tokens.RightParen tok) {
        return basicToken("RParenToken", tok);
    }

    @Override
    public String visitSet(Tokens.Set tok) {
        return basicToken("SetToken", tok);
    }

    @Override
    public String visitStr(Tokens.Str tok) {
        return "<StrToken line=" + tok.line + " col=" + tok.col + " val='" + escape(tok.literal) + "' />";
    }

    @Override
    public String visitVector(Tokens.Vec tok) {
        return basicToken("VectorToken", tok);
    }

    @Override
    public String visitError(Tokens.Error tok) {
        return "<ErrorToken line=" + tok.line + " col=" + tok.col + " val='" + escape(tok.message) + "' />";
    }
}