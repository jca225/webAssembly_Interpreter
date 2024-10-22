package edu.lehigh.cse262.slang;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Scanner;

/**
 * SourceLoader is responsible for getting code as a String and passing it to
 * the rest of the interpreter. It does extremely little syntactic analysis.
 */
public class SourceLoader implements AutoCloseable {
    /** We use a `Scanner` to read from stdin when in REPL mode */
    private Scanner inputScanner = new Scanner(System.in);

    /**
     * Get a line of text from stdin
     *
     * @param prompt A prompt to display, so the user knows to enter something
     *
     * @return A String that is expected to be some Scheme code, or `""`.
     */
    public String getFromStdin(String prompt) {
        System.out.print(prompt);
        System.out.flush();
        if (!inputScanner.hasNextLine())
            return "";
        return inputScanner.nextLine().trim();
    }

    /**
     * Read the entire contents of a file as a String
     *
     * @param fileName The name of the file to open
     *
     * @return An empty string (`""`) on any error. Otherwise, the contents of
     *         the file
     */
    public String getFile(String fileName) {
        try {
            Path path = Path.of(fileName);
            return Files.readString(path);
        } catch (Exception ex) {
            System.out.println("Error: Unable to open " + fileName);
            return "";
        }
    }

    /**
     * When the interpreter is done, it is supposed to call this, to release
     * resources. Since we implement AutoCloseable, try-with-resources does it
     * for us.
     */
    public void close() {
        inputScanner.close();
    }
}