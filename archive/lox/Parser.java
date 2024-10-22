import java.util.List;



abstract class Expr {
    /*
     * Our grammer forms a tree, since there is a lot of recursion
     * (I suspect tail-recursion will be vital in this assignment).
     * This structure represents our syntax, and thus it is called a 
     * syntax tree. We define a base class for expressions. Then, for each 
     * kind of expression -- dach production under expression -- we create
     * a subclass that has fields for the nonterminals specific to that rule.
     * This way, we get a compile error if we, say, try to access the second operand
     * of a unary expression.
     * 
     * `Expr` is the base class that all expressions inherit from.
     * The subclasses are nested inside of this.
     */
    static class Binary extends Expr {
        Binary(Expr left, Token operator, Expr right) {
            this.left = left;
            this.operator = operator;
            this.right = right;
        }

        final Expr left;
        final Token operator;
        final Expr right;
    }
}


public class Parser {
    private final List<Tokens> tokens;
    private int current = 0;

    Parser(List<Token> tokens) {
        this.tokens = tokens;
    }

    /*
     * We are going to run straight through the expression grammar
     * now and translate each rule to java code. The first rule, `expression,`
     * simply expands to the equality rule, so that's straightforward
     */
    private Expr expression() {
        return equality();
    }

    private Expr equality() {
        /*
         * This nonterminal in the body translates
         * to the first call to `comparison()` in the method.
         * We take the result and store it in a local variable.
         * 
         * Then, the ( ... )* loop in the rule maps to a while loop.
         * We need to know when to exit that loop. We can see that inside
         * the rule, we must first find either a `!=` or `==` token. So, if we
         * don't see one of those, we must be done with the sequence of equality
         * operators. We express that check using a handy `match()` method. 
         */
        Expr expr = comparison();

        while (match(BANG_EQUAL, EQUAL_EQUAL)) {
            Token operator = previous();
            Expr right = comparison();
            expr = new Expr.Binary(expr, operator, right);
        }

        return expr;
    }

    private boolean match(TokenType... types) {
        for (TokenType type : types) {
            if (check(types)) {
                advance();
                return true;
            }
        }
        return false;
    }

    private boolean check(TokenType type) {
        if (isAtEnd()) return false;
        return peek().type == type;
    }

    private Token advance() {
        if (!isAtEnd()) current++;
        return previous;
    }

    private boolean isAtEnd() {
        return peek().type == EOF;
    }

    private Token peek() {
        return tokens.get(current);
    }

    private Token previous() {
        return tokens.get(current - 1);
    }


    /*
     * The following three methods capture 
     * all of the binary operators, parsed with the correct
     * precedence and associativity. We're crawling up the precedence
     * hierarchy and now we've reached the unary operators
     */
    /*
     * This rule:
     * comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
     * Translated in java:
     * 
     * This grammar rule is virtually identical 
     */

     private Expr comparison() {
        Expr expr = term();

        while (match(GREATER, GREATER_EQUAL, LESS, LESS_EQUAL)) {
            Token operator = previous();
            Expr right = term();
            expr = new Expr.Binary(expr, operator, right);
        }

        return expr;
    }

    // first addition and subtracting
    private Expr term() {
        Expr expr = factor();

        while (match(PLUS, MINUS)) {
            Token operator = previous();
            Expr right = factor();
            expr = new Expr.Binary(expr, operator, right);
        }

        return expr;
    }

    // And finally multiplication and divison
    private Expr factor() {
        Expr expr = unary();

        while (match(SLASH, STAR)) {
            Token operator = previous();
            Expr right = unary();
            expr = new Expr.Binary(expr, operator, right);
        }

        return expr;
    }


    private Expr unary() {
        if (match(BANG, MINUS)) {
            Token operator = previous();
            Expr right = unary();
            return new Expr.Unary(operator, right);
        }

        return primary();
    }



}
