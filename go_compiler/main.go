package main

import (
	"main/scanner";
	"main/parser";
    "main/interpreter";
    "os";
    "fmt";
    "strconv";
)

/*
    is there run time type information like if it is a certain type
    cast interface type to what it really is
    type switch.
*/

func main() {
	// Open the file
    filePath := "/Users/johncabrahams/Desktop/Projects/Research Project/go_compiler/fib.wat"
	file, _ := os.ReadFile(filePath)

    // Convert to string and print
    sourceCode := string(file)
    

	scannerInstance := scanner.Scanner{
        CurrentIndex: 0,
        Source:       sourceCode,
        Line:         1,
        Tokens:       []scanner.Token{},
    }

    env := parser.Env{
        Types:    make(map[int]*string),
        Funcs:    make(map[int]*string),
        Tables:   make(map[int]*string),
        Mems:     make(map[int]*string),
        Globals:  make(map[int]*string),
        Elems:    make(map[int]*string),
        Data:     make(map[int]*string),
        Typedefs: make(map[int]*string),
    }

	tokenStream := scannerInstance.ScanTokens()

    parserInstance := parser.Parser{
        Tokens: scanner.TokenStream{},
        IdentifierContext: env,
        LabelIndex: 0,
    }
    ast := parserInstance.Parse(tokenStream)

    funcName := "fib"
    interpreter := new(interpreter.Interpreter)
    interpreter.Instantiate(ast)
    result := interpreter.CallExtern(funcName, 35)
    fmt.Println(strconv.Itoa(result[0]))


}