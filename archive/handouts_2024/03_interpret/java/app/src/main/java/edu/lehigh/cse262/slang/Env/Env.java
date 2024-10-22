package edu.lehigh.cse262.slang.Env;

import java.util.HashMap;

import edu.lehigh.cse262.slang.Parser.IValue;
import edu.lehigh.cse262.slang.Parser.Nodes;

/**
 * Env is the environment, or scope. It is a mapping from names to IValues, and
 * Envs can be stitched together in a cactus shape.
 */
public class Env {
    /** The mapping from names to expressions */
    private HashMap<String, IValue> map = new HashMap<>();

    /** The enclosing environment */
    private Env outer = null;

    /**
     * An object that represents false (#f)
     *
     * [CSE 262] Your interpreter will be much easier if there is only one
     * Symbol for #f in the entire interpreter.
     */
    public final Nodes.Bool poundF;

    /**
     * An object that represents true (#t)
     *
     * [CSE 262] Your interpreter will be much easier if there is only one
     * Symbol for #t in the entire interpreter.
     */
    public final Nodes.Bool poundT;

    /**
     * An object that represents an empty list
     * 
     * [CSE 262] Output is a lot easier if we distinguish between "null" return
     * values and returning an empty list, but we also want all empty lists to be
     * the same.
     */
    public final Nodes.Cons empty;

    /**
     * The default-constructed environment can only be made by calling
     * makeDefault(). It defines the one and only instance of `#f`
     */
    private Env(Nodes.Bool poundF, Nodes.Bool poundT, Nodes.Cons empty) {
        this.poundF = poundF;
        this.poundT = poundT;
        this.empty = empty;
    }

    /**
     * Add a key/value pair to the Environment
     *
     * @param key  The string name
     * @param expr The expression that serves as the value
     */
    public void put(String key, IValue expr) {
        map.put(key, expr);
    }

    private IValue outerGet(String key) throws Exception {
        if (outer == null)
            throw new Exception(key + " not defined at outermost scope");
        return outer.get(key);
    }

    /**
     * Get the value for a given key. If the key isn't mapped in this scope,
     * look in outer scopes.
     *
     * @param key The key to look up
     *
     * @return The value associated with the key
     */
    public IValue get(String key) throws Exception {
        var res = map.get(key);
        return (res == null) ? outerGet(key) : res;
    }

    /**
     * Update the value for a given key. Throw an exception if the key isn't
     * mapped.
     *
     * @param key  The key to update
     * @param expr The new value for the key
     */
    public void update(String key, IValue expr) {
        if (map.get(key) != null)
            map.put(key, expr);
        else
            outer.update(key, expr);
    }

    /**
     * Create the default environment
     *
     * @return An environment object that is populated with default methods for
     *         the built-in functions
     */
    public static Env makeDefault() {
        var poundF = new Nodes.Bool(false);
        var poundT = new Nodes.Bool(true);
        var empty = new Nodes.Cons((IValue) null, (IValue) null);
        var e = new Env(poundF, poundT, empty);
        LibMath.populate(e.map, e.poundT, e.poundF);
        LibLists.populate(e.map, e.poundT, e.poundF, empty);
        LibString.populate(e.map, poundT, poundF);
        LibVector.populate(e.map, poundT, poundF);
        return e;
    }

    /**
     * Create a nested (inner) environment, suitable for a lambda
     *
     * @param outer The enclosing environment
     */
    public static Env makeInner(Env outer) {
        var e = new Env(outer.poundF, outer.poundT, outer.empty);
        e.outer = outer;
        return e;
    }
}