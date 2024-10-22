package edu.lehigh.cse262.slang.Env;

import java.util.HashMap;
import java.util.List;

import edu.lehigh.cse262.slang.Parser.IValue;
import edu.lehigh.cse262.slang.Parser.Nodes;

/**
 * The purpose of LibMath is to implement all of the standard library functions
 * that we can do on numbers (Integer or Double)
 */
public class LibMath {
    /**
     * Populate the provided `map` with a standard set of mathematical functions
     */
    public static void populate(HashMap<String, IValue> map, Nodes.Bool poundT, Nodes.Bool poundF) {
        // As a starting point, let's go ahead and put the addition function
        // into the map. This will make it **much** easier to test `apply`, and
        // should provide some useful guidance for making other functions.
        //
        // Note that this code is **very** tedious. Making some helper
        // functions would probably be wise, but it's up to you to figure out
        // how.
        var add = new Nodes.BuiltInFunc("+", (List<IValue> args) -> {
            // Type checking: make sure we only have int and dbl arguments. We also will use
            // this to know if we should be returning an Int or a Dbl
            int intCount = 0;
            int dblCount = 0;
            for (var arg : args) {
                if (arg instanceof Nodes.Int)
                    intCount++;
                if (arg instanceof Nodes.Dbl)
                    dblCount++;
            }
            if (args.size() > (intCount + dblCount))
                throw new Exception("+ can only handle Int and Dbl arguments");
            // Semantic analysis: make sure there are arguments!
            if (args.size() == 0)
                throw new Exception("+ expects at least one argument");
            // Compute, making sure to know the return type
            if (dblCount > 0) {
                double result = 0;
                for (var arg : args) {
                    if (arg instanceof Nodes.Int)
                        result += ((Nodes.Int) arg).val;
                    else
                        result += ((Nodes.Dbl) arg).val;
                }
                return new Nodes.Dbl(result);
            } else {
                int result = 0;
                for (var arg : args) {
                    result += ((Nodes.Int) arg).val;
                }
                return new Nodes.Int(result);
            }
        });

        map.put(add.name, add);

    }
}
