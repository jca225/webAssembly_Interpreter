package edu.lehigh.cse262.slang;

import edu.lehigh.cse262.slang.Env.Env;
import edu.lehigh.cse262.slang.Interpreter.AstToScheme;
import edu.lehigh.cse262.slang.Interpreter.ExprEvaluator;
import edu.lehigh.cse262.slang.Parser.Nodes;
import edu.lehigh.cse262.slang.Parser.XmlToAst;

/**
 * Slang is the entry point into our Scheme parser
 */
public class Slang {
    public static void main(String[] args) {
        var parsedArgs = new Args(args);

        // If help was requested, print help and then exit immediately
        if (parsedArgs.mode == Args.Modes.HELP) {
            Args.printHelp();
            return;
        }

        // Create a SourceLoader and use it to start loading code and scanning /
        // parsing / interpreting it. When given a file, we run exactly one
        // iteration. Otherwise, we run until we get an empty string of text
        // from the sourceLoader.
        //
        // [CSE 262] You should be sure to understand this try-with-resources
        // syntax.
        try (var sourceLoader = new SourceLoader()) {
            // [CSE 262] You should be sure to understand why we make the
            // environment here
            var defaultEnvironment = Env.makeDefault();

            do {
                // Get the code to run, break if no code is available
                String codeToRun;
                if (!parsedArgs.fileName.equals(""))
                    codeToRun = sourceLoader.getFile(parsedArgs.fileName);
                else {
                    System.out.println("Reading input from stdin is not supported in p4.  Please exit and try again");
                    break;
                }
                if (codeToRun.equals(""))
                    break;

                try {
                    // SCAN mode
                    if (parsedArgs.mode == Args.Modes.SCAN) {
                        throw new Exception("-scan is not supported in p4.  Please exit and try again.");
                    }

                    // PARSE mode
                    if (parsedArgs.mode == Args.Modes.PARSE) {
                        throw new Exception("-parse is not supported in p4.  Please exit and try again.");
                    }

                    // INTERPRET mode
                    if (parsedArgs.mode == Args.Modes.INTERPRET) {
                        var expressions = new XmlToAst(defaultEnvironment.poundT, defaultEnvironment.poundF,
                                defaultEnvironment.empty).parse(codeToRun);
                        var resultPrinter = new AstToScheme(defaultEnvironment.empty);
                        ExprEvaluator evaluator = new ExprEvaluator(defaultEnvironment);
                        for (var expr : expressions) {
                            var result = expr.visitValue(evaluator);
                            if (result != null)
                                System.out.println("; " + ((Nodes.BaseNode) result).visitString(resultPrinter) + "");
                        }
                    }

                    // FULL mode
                    if (parsedArgs.mode == Args.Modes.FULL) {
                        throw new Exception("-full is not supported in p4.  Please exit and try again.");
                    }
                } catch (Exception e) {
                    // NB: If the scanner, parser, and evaluator are functioning
                    // correctly, the only exceptions that should be thrown are
                    // deliberate, and the proper recovery is to simply print a
                    // message and then resume the repl loop.
                    System.out.println(e.getMessage());
                }
            } while (parsedArgs.fileName.equals(""));
        }
    }
}
