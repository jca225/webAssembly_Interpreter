# CSE 262: Programming Assignment 3: Python

In this folder, you should implement a parser for slang in Python.  You should
be sure to use the `Grammar.md` file in the `specifications` folder to guide
your work.

Unlike the `java` folder, there is very little scaffolding in this folder.
That is intentional.  You should decide how you want to approach this
problem.  When you have a fully working Java solution, one approach is to
simply *translate* your code into Python.  Doing so is not especially
idiomatic, and will lead to you writing a lot more code than is necessary.
The more you stray from your Java design, the more you will learn, because
you will be developing directly in a dynamically typed language.  Your IDE
will be less useful, but you'll be able to do a lot more in fewer lines of
code.  For example, the reference solution is only 294 lines of code in
parser.py, plus comments.  In contrast, the Java solution has 1138 lines of
code (plus 342 lines of comments) in the `Parser` folder.

Please note that you must modify three files in this assignment:
`slang_parser.py` is where you will do most of the work, but you will need to
make a few edits to `slang_evaluator.py`, and you will need to implement the XML
output method in `slang_parser_visitors.py`.

You can run the code by typing `python3 slang.py -parse filename`, where the
filename refers to the output from a correct scanner.
