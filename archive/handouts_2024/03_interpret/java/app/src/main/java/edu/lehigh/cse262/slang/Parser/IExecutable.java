package edu.lehigh.cse262.slang.Parser;

import java.util.List;

/**
 * IExecutable allows us to wrap native functions with marshalling code for
 * managing the movement of arguments to them, and return values from them.
 */
public interface IExecutable {
    /**
     * Perform an operation using the provided arguments, in the context of the
     * given environment.
     *
     * @param args A list of (already-evaluated) values to use as arguments
     *
     * @return A value that was computed by the IExecutable
     */
    public IValue execute(List<IValue> args) throws Exception;
}
