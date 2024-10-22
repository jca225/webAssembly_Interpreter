package edu.lehigh.cse262.slang.Parser;

import java.util.ArrayList;
import java.util.List;

/**
 * XmlToAst is a lightweight parser that can convert a stream of XML that was
 * produced by AstToXml (end of parse phase) back into an abstract syntax tree
 * that is suitable for the interpretation phase.
 */
public class XmlToAst {
    /** Index of the next line to parse */
    private int next = -1;

    /**
     * The set of lines of XML that comprise the input file. Note that we assume
     * XML tokens never span a line.
     */
    private String[] lines = null;

    /** A reference to the one TRUE in the program */
    private final Nodes.Bool _true;

    /** A reference to the one FALSE in the program */
    private final Nodes.Bool _false;

    /** A reference to the one EMPTY LIST in the program */
    private final Nodes.Cons _empty;

    /**
     * Construct the XmlToAst object, which can be used to convert XML to an
     * abstract syntax tree.
     * 
     * @param _true  A reference to a Bool node for TRUE
     * @param _false A reference to a Bool node for FALSE
     * @param _empty A reference to a Bool node for an EMPTY LIST
     */
    public XmlToAst(Nodes.Bool _true, Nodes.Bool _false, Nodes.Cons _empty) {
        this._true = _true;
        this._false = _false;
        this._empty = _empty;
    }

    /** Remove escape characters from a string */
    private static String unescape(String s) {
        var unescaped = s
                .replace("\\'", "'")
                .replace("\\n", "\n")
                .replace("\\t", "\t")
                .replace("\\\\", "\\"); // must do this last!
        return unescaped;
    }

    /**
     * parse() takes a string of XML and transforms it into an AST. Unlike
     * XmlToTokens, this involves some state, so we can't get by with a static
     * method.
     *
     * NB: This code doesn't do any error checking. It is assumed that you are
     * giving it input from AstToXml, and that AstToXml is correct.
     */
    public List<Nodes.BaseNode> parse(String xml) throws Exception {
        var res = new ArrayList<Nodes.BaseNode>();
        lines = xml.split("\n");
        next = 0;
        // call into parseNext (a recursive function) to process the next
        // top-level Xml entity until we hit EOF
        while (next < lines.length)
            res.add(parseNext());
        return res;
    }

    /**
     * parseNext() is the recursive function responsible for constructing XML
     * entities. This is not pretty code: it does everything, without any
     * helpful patterns. If you wish, you can think of this as providing some
     * insight into the question "what would a parser look like if I didn't scan
     * first?"
     */
    private Nodes.BaseNode parseNext() throws Exception {
        // skip blank lines. Note that this assumes that
        while (lines[next].equals("")) {
            if (++next >= lines.length)
                throw new Exception("Unexpected end of XML stream");
        }

        // If the token has 'val' in it, find the content of the val.
        int valStart = lines[next].indexOf("val=");
        int valEnd = lines[next].length() - 3;

        // For each possible Xml tag, we parse it and make a node. In some
        // cases, we need to recurse. This logic should be pretty
        // straightforward to follow if you understand AstToXml
        if (lines[next].indexOf("<Identifier") > -1) {
            var val = unescape(lines[next++].substring(valStart + 5, valEnd - 1));
            return new Nodes.Identifier(val);
        } else if (lines[next].indexOf("<Define") > -1) {
            next++; // <Define>
            var identifier = (Nodes.Identifier) parseNext();
            var expression = parseNext();
            next++; // </Define>
            return new Nodes.Define(identifier, expression);
        } else if (lines[next].indexOf("<Bool") > -1) {
            var val = lines[next++].substring(valStart + 5, valEnd - 1);
            return val.equals("true") ? _true : _false;
        } else if (lines[next].indexOf("<Int") > -1) {
            var val = lines[next++].substring(valStart + 5, valEnd - 1);
            return new Nodes.Int(Integer.parseInt(val));
        } else if (lines[next].indexOf("<Dbl") > -1) {
            var val = lines[next++].substring(valStart + 5, valEnd - 1);
            return new Nodes.Dbl(Double.parseDouble(val));
        } else if (lines[next].indexOf("<Lambda") > -1) {
            next += 2; // <Lambda>\n<Formals>
            var formals = new ArrayList<Nodes.Identifier>();
            while (lines[next].indexOf("</Formals>") == -1)
                formals.add((Nodes.Identifier) parseNext());
            next += 2; // </Formals>\n<Expressions>
            var body = new ArrayList<Nodes.BaseNode>();
            while (lines[next].indexOf("</Expressions>") == -1)
                body.add(parseNext());
            next += 2; // </Expressions>\n</Lambda>
            return new Nodes.LambdaDef(formals, body);
        } else if (lines[next].indexOf("<If") > -1) {
            next++; // <If>
            var cond = parseNext();
            var ifTrue = parseNext();
            var ifFalse = parseNext();
            next++; // </If>
            return new Nodes.If(cond, ifTrue, ifFalse);
        } else if (lines[next].indexOf("<Set") > -1) {
            next++; // <Set>
            var identifier = (Nodes.Identifier) parseNext();
            var expression = parseNext();
            next++; // </Set>
            return new Nodes.Set(identifier, expression);
        } else if (lines[next].indexOf("<And") > -1) {
            next++; // <And>
            var expressions = new ArrayList<Nodes.BaseNode>();
            while (lines[next].indexOf("</And>") == -1)
                expressions.add(parseNext());
            next++; // </And>
            return new Nodes.And(expressions);
        } else if (lines[next].indexOf("<Or") > -1) {
            next++; // <Or>
            var expressions = new ArrayList<Nodes.BaseNode>();
            while (lines[next].indexOf("</Or>") == -1)
                expressions.add(parseNext());
            next++; // </Or>
            return new Nodes.Or(expressions);
        } else if (lines[next].indexOf("<Begin") > -1) {
            next++; // <Begin>
            var expressions = new ArrayList<Nodes.BaseNode>();
            while (lines[next].indexOf("</Begin>") == -1)
                expressions.add(parseNext());
            next++; // </Begin>
            return new Nodes.Begin(expressions);
        } else if (lines[next].indexOf("<Apply") > -1) {
            next++; // <Apply>
            var expressions = new ArrayList<Nodes.BaseNode>();
            while (lines[next].indexOf("</Apply>") == -1)
                expressions.add(parseNext());
            next++; // </Apply>
            return new Nodes.Apply(expressions);
        } else if (lines[next].indexOf("<Cons") > -1) {
            next++; // <Cons>
            IValue car = _empty;
            IValue cdr = _empty;
            if (lines[next].indexOf("<Null />") == -1)
                car = (IValue) parseNext();
            else
                next++; // consume <Null />, keep car as null
            if (lines[next].indexOf("<Null />") == -1)
                cdr = (IValue) parseNext();
            else
                next++; // consume <Null />, keep cdr as null
            next++; // </Cons>
            return (car == _empty && cdr == _empty) ? _empty : new Nodes.Cons(car, cdr);
        } else if (lines[next].indexOf("<Vector") > -1) {
            next++; // <Vector>
            var expressions = new ArrayList<IValue>();
            while (lines[next].indexOf("</Vector>") == -1)
                expressions.add((IValue) parseNext());
            next++; // </Vector>
            return new Nodes.Vec(expressions);
        } else if (lines[next].indexOf("<Quote") > -1) {
            next++; // <Quote>
            var datum = (IValue) parseNext();
            next++; // </Quote>
            return new Nodes.Quote(datum);
        } else if (lines[next].indexOf("<Tick") > -1) {
            next++; // <Tick>
            var datum = (IValue) parseNext();
            next++; // </Tick>
            return new Nodes.Tick(datum);
        } else if (lines[next].indexOf("<Char") > -1) {
            var val = unescape(lines[next++].substring(valStart + 5, valEnd - 1));
            char literal = val.charAt(0);
            if (val.equals("\\"))
                literal = '\\';
            else if (val.equals("\\t"))
                literal = '\t';
            else if (val.equals("\\n"))
                literal = '\n';
            else if (val.equals("\\'"))
                literal = '\'';
            return new Nodes.Char(literal);
        } else if (lines[next].indexOf("<Str") > -1) {
            var val = unescape(lines[next++].substring(valStart + 5, valEnd - 1));
            return new Nodes.Str(val);
        } else if (lines[next].indexOf("<Symbol") > -1) {
            var val = lines[next++].substring(valStart + 5, valEnd - 1);
            return new Nodes.Symbol(val);
        } else if (lines[next].indexOf("<Cond") > -1) {
            next++; // <Cond>
            var conditions = new ArrayList<Nodes.Cond.Condition>();
            while (lines[next].indexOf("<Condition>") > -1) {
                next += 2; // <Condition>\n<Test>
                var test = parseNext();
                next += 2; // </Test>\n<Actions>
                var expressions = new ArrayList<Nodes.BaseNode>();
                while (lines[next].indexOf("</Actions>") == -1)
                    expressions.add(parseNext());
                next += 2; // </Actions>\n</Condition>
                conditions.add(new Nodes.Cond.Condition(test, expressions));
            }
            next++; // </Cond>
            return new Nodes.Cond(conditions);
        }
        throw new Exception("Unrecognized XML tag: " + lines[next]);
    }
}