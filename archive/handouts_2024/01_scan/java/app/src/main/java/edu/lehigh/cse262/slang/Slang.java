package edu.lehigh.cse262.slang;

import edu.lehigh.cse262.slang.Scanner.Scanner;
import edu.lehigh.cse262.slang.Scanner.TokenToXml;

/**
 * JScheme is the entry point into our Scheme parser
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
            do {
                // Get the code to run, break if no code is available
                String codeToRun;
                if (!parsedArgs.fileName.equals(""))
                    codeToRun = sourceLoader.getFile(parsedArgs.fileName);
                else
                    codeToRun = sourceLoader.getFromStdin(":> ");
                if (codeToRun.equals(""))
                    break;

                // SCAN mode
                if (parsedArgs.mode == Args.Modes.SCAN) {
                    var tokens = new Scanner().scanTokens(codeToRun);
                    var printer = new TokenToXml();
                    while (tokens.hasNext()) {
                        System.out.println(tokens.nextToken().visitString(printer));
                        tokens.popToken();
                    }
                }

                // PARSE mode
                else if (parsedArgs.mode == Args.Modes.PARSE) {
                    System.out.println("-parse is not supported in p2.  Exiting...");
                    return;
                }

                // INTERPRET mode
                else if (parsedArgs.mode == Args.Modes.INTERPRET) {
                    System.out.println("-interpret is not supported in p2.  Exiting...");
                    return;
                }

                // FULL mode
                else if (parsedArgs.mode == Args.Modes.FULL) {
                    System.out.println("-full is not supported in p2.  Exiting...");
                    return;
                }
            } while (parsedArgs.fileName.equals(""));
        }
    }
}