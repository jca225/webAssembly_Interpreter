package interpreter

import (
	"main/parser"
	"main/scanner"
)

// Define our stack struct
type Stack struct {
	Stack []interface{}
}

// Function to check the first element in the stack
func (interp *Stack) peek() interface{} {
	return interp.Stack[0]
}

// Function to pop the first element in the stack
func (interp *Stack) pop() interface{} {
    // Holds the value
    var value interface{}
    // Get and remove the first value from the stack
	value, interp.Stack = interp.Stack[0], interp.Stack[1:len(interp.Stack)]
	return value
}

// Function to push an element onto the stack
func (interp *Stack) push(element interface{}) {
	interp.Stack = append([]interface{}{element}, interp.Stack...)
}

// Function to check if an element exists in a stack
func (interp *Stack) search(target interface{}) bool {
	for _, v := range interp.Stack {
        if v == target {
            return true
        }
    }
    return false
}

// Function to check if the stack is empty
func (interp *Stack) empty() bool {
	return len(interp.Stack) == 0
}

type Interpreter struct {
	// Define our stack machine
	stack Stack
	// Define our references for instances based on id
	funcInstances   map [int]parser.FuncNode
	typeInstances   map [int]parser.FunctypeNode
	exportInstances map [int]parser.ExportNode
	importInstances map [int]parser.ImportNode
	// Define our ast
	ast parser.ModuleNode
	// Define our environment
	env parser.Env
}


func (interp *Interpreter) Instantiate(ast parser.ModuleNode) {
	// Instantiate stack
	interp.stack = Stack{}
	interp.ast = ast
	interp.env = ast.Env
    interp.funcInstances = make(map[int]parser.FuncNode)
    interp.typeInstances = make(map[int]parser.FunctypeNode)
    interp.exportInstances = make(map[int]parser.ExportNode)
    interp.importInstances = make(map[int]parser.ImportNode)

	// Loop through the module fields in our AST
	for _, field := range ast.ModuleFields {
		switch f := field.(type) {
		case parser.FunctypeNode:
			interp.typeInstances[f.Id] = f
		case parser.FuncNode:
			interp.funcInstances[f.Id] = f
		case parser.ExportNode:
			interp.exportInstances[f.Id] = f
		}
	}
	

}
/* User calls an exported function. 
    funcname (string) - The name of the function to call
    args     ([]int)  - Dynamic list of arguments for the function. Arities must be equivalent
*/
func (interp *Interpreter) CallExtern(funcname string, args ...int) []int {

    // Loop through all the exported functions
    for _, export := range interp.exportInstances {
        if (funcname != export.Name) {
            continue
        }
        // Get the function corresponding to the export index
        function := interp.funcInstances[export.Id]
        // Loop through the arguments inputted
        for _, arg := range args {
            // Push the args onto the stack
            interp.stack.push(arg)
        }
        // Interpret the function
        interp.callFunc(function)
        // Define results we are to return
        var results []int
        // Loop through the results
        for _, result := range interp.stack.Stack {
            // Push the args onto the stack
            results = append(results, result.(int))
        }
        // Return the results
        return results
    }
    return []int{}
}
 
func (interp *Interpreter) callFunc(funcInstance parser.FuncNode) {
    // On each function call, we copy our base frame that will hold the current instantiation's metadata
    // This allows us to recursively call functions.
    frame := *funcInstance.Frame
    // Create a new copy of the locals. Without this, we edit the values of the locals themselves
    newLocals := make([]parser.LocalNode, len(funcInstance.Frame.Locals))

    // Copy elements from funcInstance.Frame.Locals (source) to newLocals (destination)
    copy(newLocals, funcInstance.Frame.Locals)
    frame.Locals = newLocals

    // Pop the values from the stack and store them on the local activation frame
    // NB: These are parameters, and therefore we start with index 0
    for i := 0; i < frame.ArgArity(); i++ {
        frame.SetLocalValue(interp.stack.pop().(int), i)
    }

    // Push the frame onto the stack
    interp.stack.push(frame)

    // Interpret the instructions
    interp.enterInstructionSequence(funcInstance.Instructions, &frame)
    // Determine th enumber of values returned by the function
    returnArity := frame.ReturnArity()
    // Save the return values and pop from the stack
    var returns []int
    // Loop through and add returns
    for i := 0; i < returnArity; i++ {
        returns = append(returns, interp.stack.pop().(int))
    }
    // Pop activation frame for that function
    interp.stack.pop()

    // Push return values back onto the stack
    for _, returnValue := range returns {
        interp.stack.push(returnValue)
    }

}

func (interp *Interpreter) enterInstructionSequence(code []interface{}, frame *parser.Frame) bool {
    for _, instruction := range code {
        if !interp.interpretInstruction(instruction, frame) {
            return false
        }
    }
    return true
}
/* 
    false => we exit out of the function
    true => we stay in the function
*/
func (interp *Interpreter) interpretInstruction(instruction interface{}, frame *parser.Frame) bool {
    switch instruction := instruction.(type) {
    case parser.StructuredInstructionNode:
        // Instantiate label object
        label := new(parser.Label)
        label.Instructions = instruction.Instructions
        label.ArgumentArity = 0
        label.Index = 0 
        label.LabelType = instruction.TokenType
        // Push label onto stack
        interp.stack.push(label)
        // If it returns false, then exit out of the instruction sequence
        return interp.interpretStructuredControlInstruction(frame, label)
    case parser.InstructionNode:
        switch instruction.TokenType {
        // Carry out the associated operation on our runtime structures for each instruction
        case scanner.LOCAL_GET:
            interp.stack.push(frame.GetLocal(instruction.Operand.(int)))
            return true
        case scanner.LOCAL_SET:
            frame.SetLocalValue(interp.stack.pop().(int), instruction.Operand.(int))
            return true
        case scanner.LOCAL_TEE:
            frame.SetLocalValue(interp.stack.peek().(int), instruction.Operand.(int))
            return true
        case scanner.CALL:
            // Get address of function in our store
            functionAddress := interp.env.GetIdentifierContextIndex(scanner.FUNC, instruction.Operand)
            function := interp.funcInstances[*functionAddress]
            interp.callFunc(function)
            return true
        case scanner.I32_CONST:
            interp.stack.push(instruction.Operand)
            return true
        case scanner.I32_ADD:
            interp.stack.push(interp.stack.pop().(int) + interp.stack.pop().(int))
            return true
        case scanner.GE_S:
            second := interp.stack.pop().(int)
            first := interp.stack.pop().(int)
            if first >= second {
                interp.stack.push(1)
            } else {
                interp.stack.push(0)
            }
            return true
        case scanner.I32_GT_U:
            second := interp.stack.pop().(int)
            first := interp.stack.pop().(int)
            if uint(first) > uint(second) {
                interp.stack.push(1)
            } else {
                interp.stack.push(0)
            }
            return true
        case scanner.RETURN:
            return false
        case scanner.BR_IF:
            return false
        case scanner.BR:
            return false
        }
    }
    return false
}

/* 
    True  -> jump to the position after the `end` keyword 
    False -> exit out of the function call itinterp
*/
func (interp *Interpreter) interpretStructuredControlInstruction(frame *parser.Frame, label *parser.Label) bool {
    i := 0
    for i < len(label.Instructions) {
        instruction := label.Instructions[i]
        i+=1
        // If the instruction type was not a branch instruction or return instruction, continue with normal execution
        if interp.interpretInstruction(instruction, frame) {
            continue
        }
        regularInstruction := instruction.(parser.InstructionNode)
        if regularInstruction.TokenType == scanner.BR_IF {
            // If the resulting expression we are parsing is true
            if interp.stack.pop() != 0 { // 0 - false, 1 - true
                for l := 0; l < regularInstruction.Operand.(int)+1; l++ {
                    // I.e., while the top of the stack is  value
                    for {
                        exitLoop := false
                        top := interp.stack.peek() // Peek at the top of the stack
                        // Check if the top of the stack is neither Label nor Frame
                        switch top.(type) {
                        case *parser.Label,parser.Frame:
                            exitLoop=true // Exit the loop if top is a Label or Frame
                        default:
                            interp.stack.pop() // Pop the stack if it's not a Label or Frame
                        }
                        if exitLoop {
                            break
                        }
                    }
                    // Pop the label from the stack
                    poppedLabel := interp.stack.pop()
                    if label.LabelType == scanner.LOOP {
                        interp.stack.push(poppedLabel)
                        i = 0 // Jump to the continuation of L. For a loop, this means going to the original loop index
                        continue
                    } 
                    if label.LabelType == scanner.BLOCK {
                        return true // The continuation of L is the end of the block
                    }
                }
               
            // If the result is false, continue normally
            } else {
                continue
            }
            // If it is not a branch instruction but we returned false, then it implies we must break out of all the structured control instructions.
            // This implies we return from our function call, and we must configure the stack appropriately
        } else {
            var values []interface{}
            // Pop all the values from the stack while it is not a label or frame
            // I.e., while the top of the stack is  value
            for {
                exitLoop := false
                top := interp.stack.peek() // Peek at the top of the stack
                // Check if the top of the stack is neither Label nor Frame
                switch top.(type) {
                case *parser.Label,parser.Frame:
                    exitLoop=true // Exit the loop if top is a Label or Frame
                default:
                    values = append(values, interp.stack.pop()) // Pop the stack if it's not a Label or Frame
                }
                if exitLoop {
                    break
                }
            }
            // Pop the label from the stack
            interp.stack.pop()
            // Push the values back onto the stack
            if len(values) == 0 {
                return false
            }
            if len(values) == 1 {
                interp.stack.push(values[0])
            } else {
                for i := len(values) - 1; i > 0; i-- {
                    interp.stack.push(values[i])
                }
            }
            // Exit out of structured control sequence
            return false
            
        }
        
    }
    // If we completed all of our instructions without a trap, abort, or return, then we ca continue normally
    var values []interface{}
    // Pop all the values from the stack while it is not a label or frame
    // I.e., while the top of the stack is  value
    for {
        exitLoop := false
        top := interp.stack.peek() // Peek at the top of the stack
        // Check if the top of the stack is neither Label nor Frame
        switch top.(type) {
        case *parser.Label,parser.Frame:
            exitLoop=true // Exit the loop if top is a Label or Frame
        default:
            values = append(values, interp.stack.pop()) // Pop the stack if it's not a Label or Frame
        }
        if exitLoop {
            break
        }
    }
    // Pop the label from the stack
    interp.stack.pop()
    //Push the values back onto the stack
    if len(values) == 1 {
        interp.stack.push(values[0])
    } else {
        for i := len(values) - 1; i > 0; i-- {
            interp.stack.push(values[i])
        }
    }
    return true
}


    