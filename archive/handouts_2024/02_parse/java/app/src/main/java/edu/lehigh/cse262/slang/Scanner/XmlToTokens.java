package edu.lehigh.cse262.slang.Scanner;

import java.util.ArrayList;

/**
 * XmlToTokens is a lightweight parser that can convert the stream of XML
 * entities that was produced by TokenToXml (end of scan phase) back into a list
 * of tokens that is suitable for the parse phase
 */
public class XmlToTokens {
    /** Remove escape characters from a string */
    private static String unescape(String s) {
        var unescaped = s
                .replace("'", "\\'")
                .replace("\n", "\\n")
                .replace("\t", "\\t")
                .replace("\\", "\\\\"); // must do this last!
        return unescaped;
    }

    /**
     * Since the tokens are not nested (it's a regular language, after all), we
     * don't need too much state or complexity to parse the token stream.
     *
     * NB: This code doesn't do any error checking. It is assumed that you are
     * giving it input from TokenToXml, and that TokenToXml is correct.
     */
    public static TokenStream parse(String xml) throws Exception {
        var res = new ArrayList<Tokens.BaseToken>();
        // Each line is one token
        for (var token : xml.split("\n")) {
            // Find the token type
            int firstSpace = token.indexOf(" ");
            var type = token.substring(1, firstSpace);

            // EOF is special, since it has no attributes
            if (type.equals("EofToken")) {
                res.add(new Tokens.Eof("", 0, 0));
                continue;
            }

            // Get the line and column
            int lineStart = token.indexOf("line=");
            int lineEnd = token.indexOf(" ", lineStart + 2);
            int colStart = token.indexOf("col=");
            int colEnd = token.indexOf(" ", colStart + 2);
            int line = Integer.parseInt(token.substring(lineStart + 5, lineEnd));
            int col = Integer.parseInt(token.substring(colStart + 4, colEnd));

            // Figure out where the value would be, but don't get it, since not
            // all tokens have it
            int valStart = token.indexOf("val=");
            int valEnd = token.length() - 3;

            // It's pretty straightforward to re-create the scanned tokens from
            // here
            if (type.equals("AbbrevToken")) {
                res.add(new Tokens.Abbrev("'", line, col));
            } else if (type.equals("AndToken")) {
                res.add(new Tokens.And("and", line, col));
            } else if (type.equals("BeginToken")) {
                res.add(new Tokens.Begin("begin", line, col));
            } else if (type.equals("BoolToken")) {
                var val = token.substring(valStart + 5, valEnd - 1);
                if (val.equals("true"))
                    res.add(new Tokens.Bool("#t", line, col, true));
                else
                    res.add(new Tokens.Bool("#f", line, col, false));
            } else if (type.equals("CharToken")) {
                var val = unescape(token.substring(valStart + 5, valEnd - 1));
                char literal = val.charAt(0);
                if (val.equals("\\")) {
                    literal = '\\';
                    val = "#\\\\";
                } else if (val.equals("\\t")) {
                    literal = '\t';
                    val = "#\\tab";
                } else if (val.equals("\\n")) {
                    literal = '\n';
                    val = "#\\newline";
                } else if (val.equals("\\'")) {
                    literal = '\'';
                    val = "#\\'";
                } else if (val.equals(" ")) {
                    val = "#\\space";
                } else {
                    val = "#\\" + val;
                }
                res.add(new Tokens.Char(val, line, col, literal));
            } else if (type.equals("CondToken")) {
                res.add(new Tokens.Cond("cond", line, col));
            } else if (type.equals("DblToken")) {
                var val = token.substring(valStart + 5, valEnd - 1);
                res.add(new Tokens.Dbl(val, line, col, Double.parseDouble(val)));
            } else if (type.equals("DefineToken")) {
                res.add(new Tokens.Define("define", line, col));
            } else if (type.equals("IdentifierToken")) {
                var val = unescape(token.substring(valStart + 5, valEnd - 1));
                res.add(new Tokens.Identifier(val, line, col));
            } else if (type.equals("IfToken")) {
                res.add(new Tokens.If("if", line, col));
            } else if (type.equals("IntToken")) {
                var val = token.substring(valStart + 5, valEnd - 1);
                res.add(new Tokens.Int(val, line, col, Integer.parseInt(val)));
            } else if (type.equals("LambdaToken")) {
                res.add(new Tokens.Lambda("lambda", line, col));
            } else if (type.equals("LParenToken")) {
                res.add(new Tokens.LeftParen("(", line, col));
            } else if (type.equals("OrToken")) {
                res.add(new Tokens.Or("or", line, col));
            } else if (type.equals("QuoteToken")) {
                res.add(new Tokens.Quote("quote", line, col));
            } else if (type.equals("RParenToken")) {
                res.add(new Tokens.RightParen(")", line, col));
            } else if (type.equals("SetToken")) {
                res.add(new Tokens.Set("set!", line, col));
            } else if (type.equals("StrToken")) {
                var val = unescape(token.substring(valStart + 5, valEnd - 1));
                res.add(new Tokens.Str(val, line, col, val));
            } else if (type.equals("VectorToken")) {
                res.add(new Tokens.Vec("#(", line, col));
            } else
                throw new Exception("Unrecognized type: " + type);
        }
        return new TokenStream(res);
    }
}