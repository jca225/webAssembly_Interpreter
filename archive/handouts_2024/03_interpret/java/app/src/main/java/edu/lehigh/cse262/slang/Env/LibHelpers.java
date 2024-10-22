package edu.lehigh.cse262.slang.Env;

/**
 * LibHelpers has a few static methods that are useful when defining standard
 * library functions.
 *
 * [CSE 262] You may decide not to put any common code in this file. If not,
 * that's fine.
 */
public class LibHelpers {
    /** This is like Function<>, except it can throw... */
    @FunctionalInterface
    public static interface CheckedFunction<T, R> {
        R apply(T t) throws Exception;
    }
}