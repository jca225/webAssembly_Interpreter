# CSE 262: Programming Assignment 3: Parsing "slang"

In this assignment, you will build a parser for the relatively complete subset
of the Scheme programming language that we started working with in the previous
assignment.  In order to gain experience working in new languages, you will
implement the parser twice, once in Java, and then in Python.  You will also
solve a few programs in Scheme.

## Project Details

Parsing is the second step in any compiler or interpreter.  It is the step
that turns tokens into some sort of tree structure.  Since this parser is not
connected to an interpreter, it will simply output the tree that it produces.
Java code for this output is provided.  Note that since the context free
grammar has nested constructs, the tree will not be a list: there will be
children of some nodes.

As you work on this assignment, you should try to write *idiomatic* code.
Try, as much as possible, to use language features that make your code more
readable, more familiar to experts, and more succinct and expressive.

The assignment does *not* assume that you have a working p2.  Our parser will
take as its input the *output* of the scanner.  Since your Python and Java
scanners should produce the same output, as long as one of them works for
programs that do not have invalid tokens, you should be fine.  If not, you
should ask questions on Piazza.

## What To Expect

The Java folder has the most starter code, and is probably the most approachable
part of the assignment.  It isn't "easy" to implement a parser for a
context-free language, but in Scheme, it isn't incredibly difficult either.
With just a small amount of lookahead, you should be able to correctly recognize
all of the grammar, and produce AST Nodes.  A set of test cases is provided.

Note that you are not implementing a *parse tree*, but instead an *Abstract
Syntax Tree*.  The AST is simpler than a parse tree, but this means you'll
need to be a little bit more clever as you are parsing.

After you've made progress on your Java code, you should turn to Python.
There is very little support code in the `python` folder.  That is
intentional.  You will want to think about whether the Java approach is
really right for Python or not.  In particular, Python's dynamic typing means
that you might want to just pass around hash tables, instead of having a
class hierarchy like in Java.

## Tips and Reminders

As you read through the details of this assignment, keep in mind that
subsequent assignments will build upon this... so as you craft a solution, be
sure to think about how to make it maintainable.

**Start Early**.  Just reading the code and understanding what is happening
takes time.  If you start reading the assignment early, you'll give yourself
time to think about what is supposed to be happening, and that will help you
to figure out what you will need to do.

When it comes time to implement your parser, you will probably want to do the
Java code first.  It is up to you whether to try to implement a full parser
first, and then test it, or to implement incrementally (for example, starting
with programs that just consist of a datum).  Cond is probably the most
tricky.

Note that some AST Nodes are not really for parsing, only for interpretation.
These should be easy to identify from the comments.  They are always values.

As always, please be careful about not committing unnecessary files into your
repository.

## Grading

The Java code should be the most familiar, and will be weighted the heaviest: it
will be worth 50% of your grade on this assignment.  The Python code will be
worth 35%, and the Scheme code will be worth 15%.  Please be sure to read the
per-folder README.md files for more details.

You should be sure to comment your code.  For Java and Python, comments will not
be graded extensively, only if their absence is egregious.  You may wish to use
the provided code as a reference for how I comment code, and mimic it.  In
particular, note that good comments are formatted in a way that lets the IDE
read them and build tooltips for you from them.

Please be sure to use your tools well.  For example, Visual Studio Code (and
emacs, and vim) have features that auto-format your code.  You should use these
features, so that your code is legible.

Note that some parts of the assignment, like error messages, are intentionally
vague: you need to start thinking about what it means for code to be "correct".
There are many criteria that cannot be established through unit testing.

## Collaboration and Getting Help

Students may work in teams of 2 for this assignment.  **I strongly recommend
working with a partner.**  If you plan to work in a team, you must notify me by
February 18th, so that I can set up your repository access.  If you do not send
a notification until after that date, I may deduct 10 points.  If you are
working in a team, you should **pair program** for the entire assignment. After
all, your goal is to learn together, not to each learn half the material.

If you require help, you may seek it from any of the following sources:

* The professor and TAs, via office hours or Piazza
* The Internet, as long as you use the Internet as a read-only resource and do
  not post requests for help to online sites.

It is not appropriate to share code with past or current CSE 262 students,
unless you are sharing code with your teammate.

StackOverflow is a wonderful tool for professional software engineers.  It is a
horrible place to ask for help as a student.  You should feel free to use
StackOverflow, but only as a *read only* resource.  In this class, you should
**never** need to ask a question on StackOverflow.

## Deadline

You should be done with this assignment before 11:59 PM on November 11th, 2022.
Please be sure to `git commit` and `git push` before that time, so that I can
promptly collect and grade your work.

There are many parts to this assignment, so you will probably want to `git push`
frequently.
