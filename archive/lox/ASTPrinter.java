public class ASTPrinter implements Expr.Visitor<String>{
    String print(Expr expr) {
        return expr.accept(this);
    }

    @Override
    public String visitBinaryExpr(Expr.Binary expr) {
        return parenthesize(expr.operator.lexeme,
                            expr.left, expr.right);

        
    }

    @Override
    public String visitGroupingExpr(Expr.Grouping expr) {
        return parenthesize("group", expr.expression);  
    }

    @Override
    public String visitLiteralExpr(Expr.Literal expr) {
        if (expr.value == null) return "nil";
        return expr.value.toString();

    }

    @Override
    public String visitUnaryExpr(Expr.Unary expr) {
        return parenthesize(expr.operator.lexeme, expr.right);
    }

    /*
     * Takes a name and a list of subexpressions and wraps them all up in
     * parentheses, yielding a string like:
     * 
     * (+ 1 2)
     * 
     * Note it calls `accept()` on each subexpression and passes itself. This is the recursive
     * step that lets us print an entire tree.
     * 
     */
    private String parenthesize(String name, Expr... exprs) {
        StringBuilder builder = new StringBuilder();

        builder.append("(").append(name);
        for (Expr expr : exprs) {
            builder.append(" ");
            builder.append(expr.accept(this));

        }
        builder.append(")");

        return Builder.toString();
    }
}
