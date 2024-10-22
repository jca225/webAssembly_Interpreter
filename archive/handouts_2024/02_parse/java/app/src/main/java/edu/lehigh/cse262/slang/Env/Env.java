package edu.lehigh.cse262.slang.Env;

import edu.lehigh.cse262.slang.Parser.IValue;
import edu.lehigh.cse262.slang.Parser.Nodes;

/**
 * Env is an environment, or scope. It is a mapping from names to IValues, and
 * Envs can be stitched together in a cactus shape.
 *
 * [CSE 262] While we mostly don't need the environment until we start
 * interpreting, it is beneficial to have some of the environment
 * during parsing: if our parser consistently uses the same global
 * final objects for #t, #f, and '(), then the interpreter will be
 * much easier later on.
 */
public class Env {
    /**
     * An object that represents false (#f)
     *
     * [CSE 262] We want there to be only one Symbol for #f in the entire
     * interpreter.
     */
    public final Nodes.Bool poundF;

    /**
     * An object that represents true (#t)
     *
     * [CSE 262] We want there to be only one Symbol for #t in the entire
     * interpreter.
     */
    public final Nodes.Bool poundT;

    /**
     * An object that represents an empty list, and also represents 'null'
     *
     * [CSE 262] We want all empty lists to be the same object
     */
    public final Nodes.Cons empty;

    /**
     * The default-constructed environment can only be made by calling
     * makeDefault().
     */
    private Env(Nodes.Bool poundF, Nodes.Bool poundT, Nodes.Cons empty) {
        this.poundF = poundF;
        this.poundT = poundT;
        this.empty = empty;
    }

    /**
     * Create the default environment
     *
     * @return An environment object that has #t, #f, and '()
     */
    public static Env makeDefault() {
        var poundF = new Nodes.Bool(false);
        var poundT = new Nodes.Bool(true);
        var empty = new Nodes.Cons((IValue) null, (IValue) null);
        var e = new Env(poundF, poundT, empty);
        return e;
    }
}