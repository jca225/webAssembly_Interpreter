package edu.lehigh.cse262.slang.Scanner;

/**
 * Tokens is a wrapper class. Or, if you prefer, it is a hack to get a
 * "namespace" in Java.
 *
 * The high-level goal here is to set up 20 different classes, to represent the
 * 20 different tokens that our scanner needs to understand. These tokens share
 * some common code, but are very uninteresting: they are just POJOs (plain old
 * Java objects) consisting of a few final fields and some support for the
 * visitor pattern.
 *
 * Rather than create 20 separate Java files, Tokens declares these 20 classes
 * (as well as their base class) as nested classes. These nested classes are
 * `static`, because we do not need a reference to the `Tokens` class in order
 * to make them.
 *
 * There is an extra Token type, for errors.  It should be self-explanatory.
 *
 * If you don't like this kind of code, that's OK. It's ugly. It's a bit of a
 * hack. It's just organized like this so that we don't need 21 files of
 * boilerplate code. Better yet, you don't need to edit this file, so as long as
 * you can understand what's going on here, you're good.
 */
public class Tokens {
    /**
     * BaseToken is the base class for all of the tokens that are
     * understood/recognized by our scanner. BaseToken itself is abstract, on
     * account of it not implementing the visitor pattern. However, it is not
     * just an interface, because it defines common state that is used by all of
     * its descendants.
     */
    public static abstract class BaseToken {
        /**
         * Visitor interface, for printing tokens nicely.
         *
         * [CSE 262] If you are unfamiliar with the visitor pattern, the gist of
         * it is that it is a way to avoid having big nested if statements,
         * while keeping all of the code for an operation in one place. In a bit
         * more detail, we're going to want to be able to iterate through a list
         * of tokens and print them. We might want to print them a few different
         * ways, even (text, JSON, XML, etc.). The logic for printing tokens
         * shouldn't be in the Token class. That is, we shouldn't have methods
         * like 'printAsJSON' and 'printAsXML'. But we also don't want to have
         * an object 'XmlTokenPrinter' that consists of a single method with a
         * huge if block (if this_token instanceof X else if this_token
         * instanceof Y else ...).
         *
         * [CSE 262] The visitor pattern is a sort of double indirection (don't
         * worry, in Java it's not expensive!), where the XMLPrinter will
         * implement the ITokenVisitor interface, and then pass *itself* to the
         * visit() method of the tokens. The tokens immediately "circle back" by
         * passing themselves to a more specific method of the visitor (i.e.,
         * visitX()). The net effect is that the XMLPrinter gets to keep all its
         * code in one file, but in nice, easy to understand methods.
         *
         * The only catch is that we often want visitors who produce different
         * types of results. We handle this by (1) making the interface generic,
         * and then instantiating the visitor with a specific return type, and
         * (2) putting that return type in the name of the visit function.
         * Hence, below, we have visitString().
         *
         * @param visitor The visitor object
         *
         * @return A string that was produced by the visitor
         */
        public abstract String visitString(ITokenVisitor<String> visitor);

        /** The source program characters that led to this token being made */
        public final String tokenText;

        /** The line within the source code where `tokenText` appears */
        public final int line;

        /** The column within `line` where `tokenText` appears */
        public final int col;

        /**
         * Construct a Token
         *
         * @param tokenText The string that generated the token
         * @param line      The source line of code where tokenText appears
         * @param col       The column within the source line of code
         */
        public BaseToken(String tokenText, int line, int col) {
            this.tokenText = tokenText;
            this.line = line;
            this.col = col;
        }
    }

    /** A token for `'` (quote shorthand) */
    public static class Abbrev extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Abbrev(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitAbbrev(this);
        }
    }

    /** A token for `and` (special form) */
    public static class And extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public And(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitAnd(this);
        }
    }

    /** A token for `begin` (special form) */
    public static class Begin extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Begin(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitBegin(this);
        }
    }

    /** A token for a boolean literal (`#t` or `#f`) */
    public static class Bool extends BaseToken {
        /** The logical value of this token */
        public final boolean literal;

        /**
         * Construct by saving the literal and forwarding to the Token constructor
         */
        public Bool(String tokenText, int line, int col, boolean literal) {
            super(tokenText, line, col);
            this.literal = literal;
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitBool(this);
        }
    }

    /** A token for a character literal */
    public static class Char extends BaseToken {
        /** The character value of this token */
        public final char literal;

        /**
         * Construct by saving the literal and forwarding to the Token constructor
         */
        public Char(String tokenText, int line, int col, char literal) {
            super(tokenText, line, col);
            this.literal = literal;
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitChar(this);
        }
    }

    /** A token for `cond` (special form) */
    public static class Cond extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Cond(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitCond(this);
        }
    }

    /** A token for a double (number) literal */
    public static class Dbl extends BaseToken {
        /** The double value of this token */
        public final double literal;

        /**
         * Construct by saving the literal and forwarding to the Token constructor
         */
        public Dbl(String tokenText, int line, int col, double literal) {
            super(tokenText, line, col);
            this.literal = literal;
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitDbl(this);
        }
    }

    /** A token for `define` (special form) */
    public static class Define extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Define(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitDefine(this);
        }
    }

    /** A token to represent end-of-file / end-of-input */
    public static class Eof extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Eof(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitEof(this);
        }
    }

    /**
     * A token for any identifier that isn't a literal or special form keyword. Note
     * that for Identifiers, we don't bother to save the literal. The tokenText is
     * good enough.
     */
    public static class Identifier extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Identifier(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitIdentifier(this);
        }
    }

    /** A token for `if` (special form) */
    public static class If extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public If(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitIf(this);
        }
    }

    /** A token for an integer (number) literal */
    public static class Int extends BaseToken {
        /** The integer value of this token */
        public final int literal;

        /**
         * Construct by saving the literal and forwarding to the Token constructor
         */
        public Int(String tokenText, int line, int col, int literal) {
            super(tokenText, line, col);
            this.literal = literal;
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitInt(this);
        }
    }

    /** A token for `lambda` (special form) */
    public static class Lambda extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Lambda(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitLambda(this);
        }
    }

    /** A token for `(` (start of list/expression) */
    public static class LeftParen extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public LeftParen(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitLParen(this);
        }
    }

    /** A token for `or` (special form) */
    public static class Or extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Or(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitOr(this);
        }
    }

    /** A token for `quote` (special form) */
    public static class Quote extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Quote(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitQuote(this);
        }
    }

    /** A token for `)` (end of vector/list/expression) */
    public static class RightParen extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public RightParen(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitRParen(this);
        }
    }

    /** A token for `set!` (special form) */
    public static class Set extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Set(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitSet(this);
        }
    }

    /** A token for a string (text) literal */
    public static class Str extends BaseToken {
        /** The string value of this token */
        public final String literal;

        /**
         * Construct by saving the literal and forwarding to the Token constructor
         */
        public Str(String tokenText, int line, int col, String literal) {
            super(tokenText, line, col);
            this.literal = literal;
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitStr(this);
        }
    }

    /** A token for `#(` (start of vector) */
    public static class Vec extends BaseToken {
        /** Construct by forwarding to the Token constructor */
        public Vec(String tokenText, int line, int col) {
            super(tokenText, line, col);
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitVector(this);
        }
    }

    /** A fake token for expressing a scan error */
    public static class Error extends BaseToken {
        public final String message;

        /** Construct by forwarding to the Token constructor */
        public Error(String message, int line, int col) {
            super("", line, col);
            this.message = message;
        }

        @Override
        public String visitString(ITokenVisitor<String> visitor) {
            return visitor.visitError(this);
        }
    }
}