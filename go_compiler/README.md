

RTI -> Runtime Type information

print size of instanc of struct -> returns 4
But what if method is virtual 
```C


```

virtual -> 0 overhead abstractions and if youre not using it you don't pay for it
C struct - size is governed by size and order of fields
in java we have inheritance - base class implements method and drived class overrides method and we jsut have an instance of th ebase class and is an instance of derived class.
C++ opt into that with virtual methods
anyone who derivs from my struct can override the virtual function
pointer to mystruct how do we know what type? We have a vtable pointer in the first position in the struct -- a pointer to some read-only dsta the compiler produced an dstucl into memory that tells what is the actusl type of that instance

Something attached tot he instance of the object that tells you the type of the object
In java, there is always runtime type information.
Given object ref and figure out what it is
In go, given an interface does it have runtime type informtion to figure out what it is?


Optimizer
If you have these tree transformations, does that mean you can think of `cilk_spawn` and `cilk_sync` as function calls.
These allow you to rewrite the AST.

three levels/modesl:
1. Nothing is ever shared
2. Things are not shared until sync
3. Things sre not shared until sync unless they are shared through a reducer hyperobject

Sync:
    The semantics of spawn and sync need to be defined in a way whee we can transform the AST, interrpetthe 
    trasnformed ast in parallel and produce the same result

    We are going to assume the original program is correct (i.e., race free)
    Look at a function and say, how many returns?
    spawn function call -> know where on the stack its result is supposed to go, and say, "there is no place that touches that until after the sync"
     
