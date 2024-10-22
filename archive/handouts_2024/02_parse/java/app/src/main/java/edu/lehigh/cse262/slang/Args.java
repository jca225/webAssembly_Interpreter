package edu.lehigh.cse262.slang;

/**
 * Args is an object for making sense of the command-line arguments for this
 * program.
 */
public class Args {
    /**
     * ArgType gives a programmatic name to each of the command-line options to the
     * program
     */
    public static enum Modes {
        HELP, SCAN, PARSE, INTERPRET, FULL
    }

    /**
     * Our program is a command-line program, and it can be configured by
     * passing arguments to it on the command line (such as `-help`). By
     * declaring each command-line option in one of these ArgDesc objects,
     * we can make our code a little less brittle to changes.
     *
     * Note that since the class is private to Args, we don't need to worry
     * about public/private or final qualifiers. This file should know how to
     * use this object.
     */
    private static class ArgDesc {
        /** The text of the command-line argument (e.g., `-help`) */
        final String arg;

        /** The text to display in a help message (e.g., `Display a help message` */
        final String desc;

        /** The programmatic identifier for this option */
        final Modes argId;

        /**
         * Construction an ArgDesc
         * 
         * @param arg   The argument (e.g., `-help`)
         * @param desc  The description of this command line option
         * @param argId A programmatic identifier for this command line option
         */
        ArgDesc(String arg, String desc, Modes argId) {
            this.arg = arg;
            this.desc = desc;
            this.argId = argId;
        }
    }

    /**
     * Options is a fixed array with the printable options for how to use the
     * program
     */
    private static ArgDesc[] options = {
            new ArgDesc("-help", "Display this message and exit", Modes.HELP),
            new ArgDesc("-scan", "Scan slang code, output tokens as XML", Modes.SCAN),
            new ArgDesc("-parse", "Parse from XML tokens, output an XML AST", Modes.PARSE),
            new ArgDesc("-interpret", "Interpret from XML AST", Modes.INTERPRET),
            new ArgDesc("-full", "Scan, parse, and interpret slang code", Modes.FULL),
    };

    /** Display a help message that describes how to use this program */
    public static void printHelp() {
        System.out.println("slang -- An interpreter for a subset of Scheme, written in Java");
        System.out.println("  Usage: slang [mode] [filename]");
        System.out.println("    * If no filename is given, a REPL will read and evaluate one line of stdin at a time");
        System.out.println("    * If a filename is given, the entire file will be loaded and evaluated");
        System.out.println("  Modes:");
        // Pre-compute the widths of the options, so we can have nice-looking
        // output
        int max_len = 0;
        for (var o : options)
            max_len = Math.max(max_len, o.arg.length());
        for (var o : options)
            System.out.println(String.format("    %1$-" + max_len + "s  %2$10s", o.arg, o.desc));
    }

    /** The selected mode of operation */
    public final Modes mode;

    /** The (optional) file with which to operate */
    public final String fileName;

    /**
     * Use the command-line arguments to configure this object so that it
     * describes the desired behavior of the program.
     *
     * Note: If the user does not provide any valid arguments, then the help
     * option will be enabled automatically.
     *
     * @param args The command line arguments to the program.
     */
    public Args(String[] args) {
        // Temp results while we're evaluating the args
        Modes mode = Modes.HELP;
        String fileName = "";
        // Counters for making sure the usage is correct
        int numModes = 0, numNames = 0;

        // NB: This is O(n^2), but it's OK, since `n` will never be large
        outer: for (var arg : args) {
            for (var o : options) {
                if (arg.equals(o.arg)) {
                    mode = o.argId;
                    ++numModes;
                    continue outer;
                }
            }
            fileName = arg;
            ++numNames;
        }

        // Force us into help mode if the args were not valid
        if (numModes != 1 || numNames > 1) {
            this.fileName = "";
            this.mode = Modes.HELP;
        } else {
            this.mode = mode;
            this.fileName = fileName;
        }
    }
}
