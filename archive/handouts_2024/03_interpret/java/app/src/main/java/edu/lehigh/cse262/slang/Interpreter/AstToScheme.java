package edu.lehigh.cse262.slang.Interpreter;

import edu.lehigh.cse262.slang.Parser.IAstVisitor;
import edu.lehigh.cse262.slang.Parser.Nodes;

/**
 * AstToScheme is a visitor that produces, for each AST node, a string
 * representation of that node as Scheme code. This is really only intended for
 * printing the result of an expression during REPL, but there's some
 * indentation stuff buried in here that kinda sorta prints out the structure of
 * the AST, too.
 *
 * [CSE 262] This is not very good code, and it's not very interesting. I'm not
 * going to document it.
 */
public class AstToScheme implements IAstVisitor<String> {
    private int indentation = 0;

    private boolean inList = false;

    private final Nodes.Cons empty;

    public AstToScheme(Nodes.Cons empty) {
        this.empty = empty;
    }

    private void indent(StringBuilder sb) {
        for (int i = 0; i < indentation; ++i)
            sb.append(" ");
    }

    @Override
    public String visitIdentifier(Nodes.Identifier expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append(expr.name);
        return sb.toString();
    }

    @Override
    public String visitDefine(Nodes.Define expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("(define\n");
        indentation++;
        sb.append(expr.identifier.visitString(this));
        sb.append("\n");
        sb.append(expr.expression.visitString(this));
        sb.append(")");
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitBool(Nodes.Bool expr) {
        var sb = new StringBuilder();
        indent(sb);
        sb.append(expr.val ? "#t" : "#f");
        return sb.toString();
    }

    @Override
    public String visitInt(Nodes.Int expr) {
        var sb = new StringBuilder();
        indent(sb);
        sb.append(expr.val);
        return sb.toString();
    }

    @Override
    public String visitDbl(Nodes.Dbl expr) {
        var sb = new StringBuilder();
        indent(sb);
        sb.append(expr.val);
        return sb.toString();
    }

    @Override
    public String visitLambdaDef(Nodes.LambdaDef expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("(lambda (");
        indentation++;
        for (var f : expr.formals)
            sb.append("\n" + f.visitString(this));
        sb.append(")");
        for (var e : expr.body)
            sb.append("\n" + e.visitString(this));
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitIf(Nodes.If expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("(if\n");
        indentation++;
        sb.append(expr.cond.visitString(this));
        sb.append("\n");
        sb.append(expr.ifTrue.visitString(this));
        sb.append("\n");
        sb.append(expr.ifFalse.visitString(this));
        sb.append(")");
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitSet(Nodes.Set expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("(set! \n");
        indentation++;
        sb.append(expr.identifier.visitString(this));
        sb.append("\n");
        sb.append(expr.expression.visitString(this));
        sb.append(")");
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitAnd(Nodes.And expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("(and");
        indentation++;
        for (var e : expr.expressions) {
            sb.append("\n");
            sb.append(e.visitString(this));
        }
        sb.append(")");
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitOr(Nodes.Or expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("(or");
        indentation++;
        for (var e : expr.expressions) {
            sb.append("\n");
            sb.append(e.visitString(this));
        }
        sb.append(")");
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitBegin(Nodes.Begin expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("(begin");
        indentation++;
        for (var e : expr.expressions) {
            sb.append("\n");
            sb.append(e.visitString(this));
        }
        sb.append(")");
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitApply(Nodes.Apply expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("(");
        indentation++;
        for (var e : expr.expressions) {
            sb.append("\n");
            sb.append(e.visitString(this));
        }
        sb.append(")");
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitCons(Nodes.Cons expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        if (expr == empty) {
            sb.append("()");
            return sb.toString();
        }
        boolean first = false;
        if (!inList) {
            sb.append("(");
            inList = true;
            indentation++;
            first = true;
        }
        sb.append("\n");
        var car = (Nodes.BaseNode) expr.car;
        var cdr = (Nodes.BaseNode) expr.cdr;
        if (car == null) {
            indent(sb);
            sb.append("()");
        } else if (car instanceof Nodes.Cons) {
            inList = false;
            indent(sb);
            sb.append(car.visitString(this));
            inList = true;
        } else {
            indent(sb);
            sb.append(car.visitString(this));
        }
        if (cdr != empty) {
            if (!(cdr instanceof Nodes.Cons)) {
                sb.append(".\n");
                indent(sb);
                sb.append(cdr.visitString(this));
            } else {
                indent(sb);
                sb.append(cdr.visitString(this));
            }
        }
        if (first) {
            sb.append(")");
            inList = false;
            indentation--;
        }
        return sb.toString();
    }

    @Override
    public String visitVec(Nodes.Vec expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("#(");
        indentation++;
        for (var i : expr.items) {
            sb.append("\n");
            sb.append(((Nodes.BaseNode) i).visitString(this));
        }
        sb.append(")");
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitSymbol(Nodes.Symbol expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append(expr.name);
        return sb.toString();
    }

    @Override
    public String visitQuote(Nodes.Quote expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("(quote\n");
        indentation++;
        sb.append(((Nodes.BaseNode) expr.datum).visitString(this));
        sb.append(")");
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitTick(Nodes.Tick expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("'\n");
        indentation++;
        sb.append(((Nodes.BaseNode) expr.datum).visitString(this));
        indentation--;
        return sb.toString();
    }

    @Override
    public String visitChar(Nodes.Char expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append(expr.val);
        return sb.toString();
    }

    @Override
    public String visitStr(Nodes.Str expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append(expr.val);
        return sb.toString();
    }

    @Override
    public String visitBuiltInFunc(Nodes.BuiltInFunc expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("Built-in Function (");
        sb.append(expr.name);
        sb.append(")");
        return sb.toString();
    }

    @Override
    public String visitLambdaVal(Nodes.LambdaVal val) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("Lambda with " + val.lambda.formals.size() + " args");
        return sb.toString();
    }

    @Override
    public String visitCond(Nodes.Cond expr) throws Exception {
        var sb = new StringBuilder();
        indent(sb);
        sb.append("(cond");
        indentation++;
        for (var cond : expr.conditions) {
            sb.append("\n");
            indent(sb);
            sb.append("(\n");
            indentation++;
            sb.append(cond.test.visitString(this));
            for (var e : cond.expressions) {
                sb.append("\n");
                sb.append(e.visitString(this));
            }
            indentation--;
            sb.append(")");
        }
        sb.append(")");
        indentation--;
        return sb.toString();
    }
}