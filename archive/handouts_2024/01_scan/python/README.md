# CSE 262: Programming Assignment 2: Scanning Slang in Python

In this folder, you should implement a scanner for slang in Python.  You should
be sure to use the documents in the `../specifications` folder to guide your
work.

Unlike the `java` folder, there is very little scaffolding in this folder.  That
is intentional.  You should decide how you want to approach this problem.  When
you have a fully working Java solution, one approach is to simply *translate*
your code into Python.  Doing so is not especially idiomatic, and will lead to
you writing a lot more code than is necessary.  The more you stray from your
Java design, the more you will learn, because you will be developing directly in
a dynamically typed language.  Your IDE will be less useful, but you'll be able
to do a lot more in fewer lines of code.  For example, the reference solution is
only 298 lines of code, plus comments.  In contrast, the Java solution has 686
lines of code (plus 439 lines of comments) in the `Scanner` folder.

You can run the code in interactive mode by typing `python3 slang.py -scan`.
To scan a file directly, provide a file name, e.g., by typing `python3
slang.py -scan ../tests/scan/fail_char_1.scm`.
