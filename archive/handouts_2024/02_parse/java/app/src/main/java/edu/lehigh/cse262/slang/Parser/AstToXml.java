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