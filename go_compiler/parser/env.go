package parser

import "main/scanner"

// Create the methods for our environment method
type EnvInterface interface {
	getContext(context string) map[int]*string 
    getIdentifierContext(identifierType string, identifier interface{}) interface{}
    addIdentifierContext(identifierType string, identifier *string) int
}

// Struct to hold the identifier context for our module. dictionary represents and index space. When we would like to know
// What an id is referencing, we look for it inside the environment
type Env struct {
	Types map[int]*string
    Funcs map[int]*string
    Tables map[int]*string
    Mems map[int]*string
    Globals map[int]*string
    Elems map[int]*string
    Data map[int]*string
    Typedefs map[int]*string
}

// Method to get the context pertaining to a string input. They are now able to read and write
// to the corresponding context.
func (e Env) getContext(identifierType int) *map[int]*string  {
    switch identifierType {
    case scanner.TYPE:
        return &e.Types
    case scanner.FUNC:
        return &e.Funcs
    case scanner.TABLE:
        return &e.Tables
    case scanner.MEMORY:
        return &e.Mems
    case scanner.GLOBAL:
        return &e.Globals
    }
    return nil
}

// Method to get the corresponding identifier index for a certain context space
func (e Env) GetIdentifierContextIndex(identifierSpace int, identifier interface{}) *int {
    identifierTypeMap := *e.getContext(identifierSpace)
    switch identifier.(type) {
    case int:
        index, _ := identifier.(int)
        return &index
    case string:
        // Iterate through the map
        for index, indexedIdentifier := range identifierTypeMap {
            if *indexedIdentifier == identifier.(string) {
                return &index
            }
        }
    }
    return nil
}

// Method to add an identifier to an identifier context 
func (e *Env) AddIdentifierContext(identifierSpace int, identifier *string) int {
    identifierTypeMap := *e.getContext(identifierSpace)
    index := len(identifierTypeMap)
    identifierTypeMap[index] = identifier
    return index
}

// Struct to hold our environment for functions
type Frame struct {
    Locals []LocalNode
    labels []int
    returns []ReturnNode
    args []LocalNode

}

// Holds the methods that will interact with our frame
type FrameInterface interface {
    ReturnArity() int
    SetLocal(value int)
    SetLocalValue(value int, index int)
    GetLocal(index int)
    AddArg(arg LocalNode)
    AddReturn(valType int)
    ArgArity() int
    LocalArity() int
}

// Return the number of returns for the frame
func (f *Frame) ReturnArity()int {
    return len(f.returns)
}

// Add a new local node to our list of locals
func (f *Frame) SetLocal(value LocalNode) {
    f.Locals = append(f.Locals, value)
}

/* Add a new value to a certain local node
    value - value to set it to
    index - position in locals
*/
func (f *Frame) SetLocalValue(value int, index int) {
    f.Locals[index].Value = value
}

// Get the value associated with a certain local
func (f *Frame) GetLocal(index int) int {
    return f.Locals[index].Value
}

// Add an argument to the list of arguments
func (f *Frame) AddArgument(arg LocalNode) {
    f.args = append(f.args, arg)
}

// Add a return value to the list of returns
func (f *Frame) AddReturn(valtype int) {
    f.returns = append(f.returns, ReturnNode{TokenType:valtype})
}

// Get the arity of the arguments
func (f *Frame) ArgArity() int {
    return len(f.args)
}

// Label will hold information regarding our block instruction
type Label struct {
    Instructions []interface{} 
    ArgumentArity int
    Index int
    LabelType int
}

