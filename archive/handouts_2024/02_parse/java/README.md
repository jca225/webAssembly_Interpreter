# CSE 262: Programming Assignment 3: Java

In this folder, you should implement a parser for slang in Java.  You should be
sure to use the `Grammar.md` file in the `specifications` folder to guide your
work.

Please be sure to read the code in the `app` folder before you start.  There
are about 1180 lines of code that we provide, that you do not need to edit.
The only file you should edit is the `Parser.java` file.

Note that in this assignment, your parser will output XML-like data.  It won't
actually execute any Scheme code.

You can build the code by typing `./gradlew build`.  To run it, provide a file
name, i.e., by typing `java -jar app/build/libs/app.jar -parse filename`, where
the filename is the output from a correct scanner (from assignment 2).
