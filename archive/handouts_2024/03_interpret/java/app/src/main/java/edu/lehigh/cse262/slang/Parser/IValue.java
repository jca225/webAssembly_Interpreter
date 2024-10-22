package edu.lehigh.cse262.slang.Parser;

/**
 * IValue is an empty interface, but it is quite useful. Some of our AstNodes
 * implement this interface, which means that they can be considered values, as
 * well as expressions. Examples include numbers, characters, strings, symbols,
 * booleans, lists, vectors, and built-in functions.
 *
 * By tagging these AstNodes as IValue, we can more easily discover
 * circumstances in which we are mistaking an Expression for a Value. This, in
 * turn, helps detect when we've written the compiler incorrectly, and it is
 * thus not evaluating deeply enough, or is double-evaluating.
 */
public interface IValue {
}
