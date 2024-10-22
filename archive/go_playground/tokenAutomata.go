"""The following structs define the finite automata for our tokens"""
string = {
    "startState" : "\"",
    "acceptingState" : "\"",
    "transitionFn" : {"\\": "\""}
}

type finiteAutomata struct {
	startState *str
	acceptingState *str
	transitionFunction *str
}

lineComment = {
    "startState" : ";;",
    "acceptingState" : "\n",
    "transitionFn" : None
}

blockComment = {
    "startState" : "(;",
    "acceptingState" : ";)",
    "transitionFn" : None
}

keyword = {
    "startState" : [chr(a) for a in range(97,123)],
    "acceptingState" : None,
    "transitionFn" : [chr(a) for a in range(97,123)] + [chr(a) for a in range(65,91)] + [str(a) for a in range(0,10)] + ['!', '#', '$', '%', '&', '`', '*', '-', '+', '.', '/', ':', '<', '=', '>', '?', '@', '\\', '^', '\'', '_', '|', '~']
}

integer = {
    "startState" : ['+', '-'] + [str(a) for a in range(0,10)],
    "acceptingState" : None,
    "transitionFn" : ['_'] + [str(a) for a in range(0,10)]
}

id = {
    "startState" : '$',
    "acceptingState" : None,
    "transitionFn" : ['!', '#', '$', '%', '&', '`', '*', '-', '+', '.', '/', ':', '<', '=', '>', '?', '@', '\\', '^', '\'', '_', '|', '~'] + [chr(a) for a in range(97,123)] + [chr(a) for a in range(65,91)] + [str(a) for a in range(0,10)]
}