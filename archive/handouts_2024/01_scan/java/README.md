# CSE 262: Programming Assignment 2: Scanning Slang in Java

In this folder, you should implement a scanner for slang in Java.  You should be
sure to use the documents in the `../specifications` folder to guide your work.

Please be sure to read the code in the `app` folder before you start.  There are
about 480 lines of code that we provide, that you do not need to edit.  The only
file you should edit is the `Scanner.java` file.

You should test your code by using the tests in the `../tests/scan` folder.

Note that in this assignment, your scanner will output XML-like data.  It won't
actually execute any Scheme code.

You can build the code by typing `./gradlew build`.  To run it in interactive
mode, type `java -jar app/build/libs/app.jar -scan`.  To scan a file directly,
provide a file name, i.e., by typing `java -jar app/build/libs/app.jar -scan
../tests/scan/fail_char_1.scm`.
