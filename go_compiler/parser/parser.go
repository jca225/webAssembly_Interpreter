package parser

import (
	"main/scanner"
)

// Parser structure holds relevant variables for our parser
type Parser struct {
	Tokens scanner.TokenStream
	IdentifierContext Env
	LabelIndex int
}

// Parser interface holds relevant methods for parsing
type ParserInterface interface {
	Parse(tokens []scanner.TokenStream) ModuleNode
	parseModuleField() interface{}
	parseFunc() FuncNode
	parseOptionalIdentifier(tokenType int) int
	parseIndex(tokenType int) int
	parseType() FunctypeNode
	parseFunctype() Frame
	parseTypeUse() 
	parseParams(Frame)
	parseLocals(Frame)
	parseResults(Frame)
	parseInstruction() InstructionNode
	parseImport()
	parseImportDescendant()
	checkOpenParentheses() bool
	checkCloseParentheses() bool 
	checkKeyword() bool

}

// Takes as input a stream of tokens and returns a module node representing the AST of that token stream
func (p *Parser) Parse(tokens scanner.TokenStream) ModuleNode {
	// Define tokens for our parser
	p.Tokens = tokens
	var moduleId interface{} // Module id can be int or string
	var moduleFields []interface{} // Module fields can take on multiplem types
	// Parse module (must be opening parentheses and module keyword)
	if p.checkOpenParentheses() && p.checkKeyword(scanner.MODULE) {
		// If the next token type is an identifier
		if (p.Tokens.NextToken().TokenType == scanner.IDENTIFIER) {
			moduleId = p.Tokens.NextToken().Literal
		}
		// Parse the module field
		moduleFields = p.parseModuleFields()
	}
	// Assert closing parentheses
	p.checkCloseParentheses()
	return ModuleNode{Id: moduleId, ModuleFields: moduleFields, Env: p.IdentifierContext}
}

// Parses the module fields, our second layer in the parser 
func (p *Parser) parseModuleFields() []interface{} {
	// Create an empty module fields array with any type
	var moduleFields []interface{} = make([]interface{}, 0)
	// Create an empty module field with any time
	var moduleField interface{}
	// Check for opening parentheses
	for p.checkOpenParentheses() {
		// Switch between different parsing methods and therefore different returned nodes depending on the keyword type
		switch p.Tokens.NextToken().TokenType {
		case scanner.FUNC:
			p.Tokens.PopToken() // Pop the token
			moduleField = p.parseFunc()
		case scanner.EXPORT:
			p.Tokens.PopToken() // Pop the token
			moduleField = p.parseExport()
		case scanner.TYPE:
			p.Tokens.PopToken() // Pop the token
 			moduleField = p.parseType()
		case scanner.IMPORT:
			p.Tokens.PopToken() // Pop the token
			moduleField = p.parseImport()
		}
		// Append the newly creating module field
		moduleFields = append(moduleFields, moduleField)
	} 
	return moduleFields

}

// Parse function with instructions
func (p *Parser) parseFunc() FuncNode {
	// Add id to global identifier context for our module
	id := p.parseOptionalIdentifier(scanner.FUNC)
	// Create type index and frame
	typeidx, frame := p.parseTypeUse()
	// Parse the locals
	p.parseLocals(frame)
	// Initialize list of instructions
	var instructions []interface{}
	// Parse instructions while there is no closing parenthese
	for !p.checkCloseParentheses() {
		instructions = append(instructions, p.parseInstruction())
	}
	// Reset label index
	p.LabelIndex = 0
	// Return Func Node
	return FuncNode{Id: id, TypeIndex: typeidx, Frame: frame, Instructions: instructions}
}

// Parse optional identifier (i.e., of the form id^?, meaning there may or may not be an id)
func (p *Parser) parseOptionalIdentifier(tokenType int) int {
	// Checking if there is an id is easily verifiable by the next tokens type
	if p.Tokens.NextToken().TokenType == scanner.IDENTIFIER {
		// Convert to string. always true based on our token stream invariant for identifiers
		identifier, _ := p.Tokens.NextToken().Literal.(string)
		p.Tokens.PopToken() // pop the token
		// Add the identifier to the identifier context. Index it was added at is returned
		return p.IdentifierContext.AddIdentifierContext(tokenType, &identifier)
	}
	// Add the identifier to the identifier context. Index it was added at is returned
	// `nil` implies there is no associated identifier with the node we are parsing
	return p.IdentifierContext.AddIdentifierContext(tokenType, nil)
}

func (p *Parser) parseIdx(tokenType int) int {
	identifier := p.Tokens.NextToken().Literal
	p.Tokens.PopToken()
	return *p.IdentifierContext.GetIdentifierContextIndex(tokenType, identifier)
	
}

/* Takes as input type definition of a function. Adds the typedef to the identifier context and returns the node */
func (p *Parser) parseType() FunctypeNode {
	// Add id to global identifier context for our module
	id := p.parseOptionalIdentifier(scanner.TYPE)
	// Pop left parentheses and FUNC keyword
	p.Tokens.PopToken()
	p.Tokens.PopToken()
	// Parse func type. We do no verifying and simply use this as a 
	// means to consume the necessary amount of tokens
	_ = p.parseFunctype()
	// Get closing parentheses for functype
	p.checkCloseParentheses()
	// Return type node
	return FunctypeNode{Id: id}
}

// Create a new frame according to the parameters and results in our functype
func (p *Parser) parseFunctype() *Frame {
	// Parse frame
	frame := new(Frame)
	// Parse params and edit frame appropriately
	p.parseParams(frame)
	// Parse results and edit frame appropriately
	p.parseResults(frame)
	// Check for closing parentheses for func def
	p.checkCloseParentheses()
	return frame
}

// Parse type use. Refers to the use of a previously defined Functype.
// Returns parsed frame based on functype and index of the functype 
func (p *Parser) parseTypeUse() (int, *Frame) {
	// Assert opening parentheses
	p.checkOpenParentheses()
	// Create new call frame
	frame := new(Frame)
	// If type keyword exists then it is a new type and we must add it to the list of typeuses.
	// Our implementation deems that step unneccessary and we simply produce the corresponding frame and type index
	// associated with the type use. In other words, we add the type index to our identifier context but do not 
	// reference it in the interpeter
	if p.checkKeyword(scanner.TYPE) {
		// Add mapping to the global identifier context
		parsedTypeIdx := p.parseIdx(scanner.TYPE)
		// Assert closing parentheses for type
		p.checkCloseParentheses()
		// Parse parameters and results
		p.parseParams(frame)
		p.parseResults(frame)
		return parsedTypeIdx, frame
	// Otherwise we are referencing a type that has already been declared; We get that type index in our
	// identifier context and return it
	} else {
		p.parseParams(frame)
		p.parseResults(frame)
		// If a type index does not exist it is inserted baed on the global scope
		typeidx := p.IdentifierContext.AddIdentifierContext(scanner.TYPE, nil)
		return typeidx, frame
	}

}

// Parses abbreviated (no identifiers) or non-abbreviated (may or may not contain identifiers)
// parameters
func (p *Parser) parseParams(frame *Frame) {
	// Abbreviation mechanism; this mechanism only works for parameters with no ids.
	// It also has the property of being universally generalized: If it holds for one element 
	// then it must hold for all. Thus if it holds for the next two elements then the entire
	// vector must be an abbreviation
	if p.checkOpenParentheses() && p.checkKeyword(scanner.PARAM) {
		if (p.Tokens.NextToken().TokenType == scanner.I32 || 
		    p.Tokens.NextToken().TokenType == scanner.I64 || 
		    p.Tokens.NextToken().TokenType == scanner.F32 || 
		    p.Tokens.NextToken().TokenType == scanner.F64) && 
		   (p.Tokens.NextNextToken().TokenType == scanner.I32 || 
		    p.Tokens.NextNextToken().TokenType == scanner.I64 || 
		    p.Tokens.NextNextToken().TokenType == scanner.F32 || 
		    p.Tokens.NextNextToken().TokenType == scanner.F64) {
				// while there exists no closing parentheses parse and add locals
				for !p.checkCloseParentheses() {
					// Pop token
					p.Tokens.PopToken()
					// Add anonymous parameters of certain types to the local environment's locals
					tokenType := p.Tokens.NextToken().TokenType	
					localNode := LocalNode{TokenType: tokenType, Identifier: nil}
					frame.SetLocal(localNode)		
					frame.AddArgument(localNode)		

				}
			// Otherwise we assume there may or may not exist ids
			} else {
				// Regular parsing mechanism (i.e., no abbreviation)
				for {
					// Define id
					var id interface{}
					// define token type
					var tokenType int
					// Ids are easily verifiable
					if (p.Tokens.NextToken().TokenType == scanner.IDENTIFIER) {
						id = p.parseOptionalIdentifier(scanner.TYPE)
						// Pop the corresponding id token
						p.Tokens.PopToken()
					}
					// Get the token type
					tokenType = p.Tokens.NextToken().TokenType
					// Pop the token
					p.Tokens.PopToken()						
					// Instantiate local node
					localNode := LocalNode{TokenType: tokenType, Identifier: id}
					// Set locals and arguments
					frame.SetLocal(localNode)		
					frame.AddArgument(localNode)	
					// Pop the closing parentheses token implicitly assumed due to the invariants
					// in our scanner
					p.Tokens.PopToken()
					// If the next two tokens are not: '(' 'PARAM' then we break
					if !p.checkOpenParenthesesKeyword(scanner.PARAM) {
						break
					}
				}
			}
	}
}

func (p *Parser) parseLocals(frame *Frame) {
	// Abbreviation mechanism; this mechanism only works for **locals** with no ids.
	// It also has the property of being universally generalized: If it holds for one element 
	// then it must hold for all. Thus if it holds for the next two elements then the entire
	// vector must be an abbreviation
	if p.checkOpenParentheses() && p.checkKeyword(scanner.LOCAL) {
		if (p.Tokens.NextToken().TokenType == scanner.I32 || 
		    p.Tokens.NextToken().TokenType == scanner.I64 || 
		    p.Tokens.NextToken().TokenType == scanner.F32 || 
		    p.Tokens.NextToken().TokenType == scanner.F64) && 
		   (p.Tokens.NextNextToken().TokenType == scanner.I32 || 
		    p.Tokens.NextNextToken().TokenType == scanner.I64 || 
		    p.Tokens.NextNextToken().TokenType == scanner.F32 || 
		    p.Tokens.NextNextToken().TokenType == scanner.F64) {
				// While there are no closing parentheses indicating we are done
				for !p.checkCloseParentheses() {
					// Pop token
					p.Tokens.PopToken()
					// Add anonymous parameters of certain types tot he local environment's locals
					tokenType := p.Tokens.NextToken().TokenType	
					localNode := LocalNode{TokenType: tokenType, Identifier: nil}
					frame.SetLocal(localNode)		

				}
			} else {
				// Regular parsing mechanism (i.e., no abbreviation)
				for {
					// Define id
					var id interface{}
					// define token type
					var tokenType int
					// Ids are easily verifiable
					if (p.Tokens.NextToken().TokenType == scanner.IDENTIFIER) {
						id = p.parseOptionalIdentifier(scanner.TYPE)
						// Pop the corresponding id token
						p.Tokens.PopToken()
					}
					// Get the token type
					tokenType = p.Tokens.NextToken().TokenType
					// Pop the token
					p.Tokens.PopToken()						
					// Instantiate local node
					localNode := LocalNode{TokenType: tokenType, Identifier: id}
					// Set local 
					frame.AddArgument(localNode)	
					// Pop the closing parentheses token implicitly assumed due to the invariants
					// in our scanner
					p.Tokens.PopToken()
					// If the next two tokens are not: '(' 'PARAM' then we break
					if !p.checkOpenParenthesesKeyword(scanner.LOCAL) {
						break
					}
				}
			}
	}
}

// Method to parse results for a function
func (p *Parser) parseResults(frame *Frame) {
	// If the next two tokens are of type: '(' 'result'
	if p.checkOpenParenthesesKeyword(scanner.RESULT)  {
		// While there is no closing parentheses parse the corresponding types.
		// NB: Results cannot have identifiers. They are always anonymous
		for !p.checkCloseParentheses() {
			tokenType := p.Tokens.NextToken().TokenType
			p.Tokens.PopToken()
			frame.AddReturn(tokenType)
			
		}
	}
}

// Method to parse a singular instruction. Note the instruction may be structured or regular, and therefore
// can take on multiple types
func (p *Parser) parseInstruction() interface{} {
	// Booleans to indicate if we are dealing with a block or a loop
	block := p.checkKeyword(scanner.BLOCK)
	loop := p.checkKeyword(scanner.LOOP)
	if (block || loop) {
		// Create instructions list
		var instructions []interface{}
		// Add optional label to the local environment
		for !p.checkKeyword(scanner.END) {
			instructions = append(instructions, p.parseInstruction())
		}
		// Return corresponding structured control instruction. For now we return default label index 
		// since there are no nested control instructions in our subset of code we are able to interpret
		if block {
			return StructuredInstructionNode{scanner.BLOCK, instructions, 1}
		} else {
			return StructuredInstructionNode{scanner.LOOP, instructions, 1}
		}
	} else {
		// Get the corresponding instruction type
		instructionType := p.Tokens.NextToken().TokenType
		// Pop the token
		p.Tokens.PopToken()
		// Check to see if the instruction node has an argument
		if p.Tokens.NextToken().TokenType == scanner.IDENTIFIER || p.Tokens.NextToken().TokenType == scanner.CONST {
			operand := p.Tokens.NextToken().Literal
			p.Tokens.PopToken()
			return InstructionNode{TokenType: instructionType, Operand: operand}
		// Otherwise assume the argument is nil
		} else {
			return InstructionNode{TokenType: instructionType, Operand: nil}
		}
	}
}

// Function to parse an import node
func (p *Parser) parseImport() ImportNode {
	// Get the name of the module
	module, _ := p.Tokens.NextToken().Literal.(string)
	// Pop the token
	p.Tokens.PopToken()
	// Get the name of the import
	name := p.Tokens.NextToken().Literal.(string)
	// Pop token
	p.Tokens.PopToken()
	// Define and parse the import descendant
	importDesc := p.parseImportDesc()
	// Assert closing parentheses
	p.checkCloseParentheses()
	// Return the import node
	return ImportNode{ModuleName: module, Name: name, ImportDescendant: importDesc}
}

func (p *Parser) parseImportDesc() interface{} {
	if p.checkOpenParentheses() {
		switch p.Tokens.NextToken().TokenType {
			case scanner.FUNC:
				// Pop keyword token
				p.Tokens.PopToken()
				// Add id to global identifier context for our module
				id := p.parseOptionalIdentifier(scanner.FUNC)
				// Create type index and frame
				_, frame := p.parseTypeUse()
				// Check closing parentheses
				p.checkCloseParentheses()
				return TypeuseNode{Identifier: id, Frame: frame} 
			case scanner.MEMORY:
				// Pop keyword token
				p.Tokens.PopToken()
				// Add id to global identifier context for our module
				id := p.parseOptionalIdentifier(scanner.MEMORY)
				// Create type index and frame
				memtype := p.parseLimits()
				// Check closing parentheses
				p.checkCloseParentheses()
				return MemoryNode{Identifier: id, ValType: memtype} 
		}
	}
	// Return nothing if none of this were satisfied to satisfy compiler
	return nil
}


func (p *Parser) parseExport() ExportNode {
	name := p.Tokens.NextToken().Literal.(string)
	p.Tokens.PopToken()
	idx := p.parseExportDesc()
	return ExportNode{Name: name, Id: idx}
}

func (p *Parser) parseExportDesc() int {
	if p.checkOpenParentheses() {
		switch p.Tokens.NextToken().TokenType {
			case scanner.FUNC:
				// Pop func token
				p.Tokens.PopToken()
				// Add id to global identifier context for our module
				idx := p.parseIdx(scanner.FUNC)
				return idx

		}
	}
	return 0
}

func (p *Parser) parseLimits() LimitsNode {
	min := 0
	if p.Tokens.NextToken().TokenType == scanner.CONST {
		min, _ = p.Tokens.NextToken().Literal.(int)
		p.Tokens.PopToken()
	}
	if p.Tokens.NextToken().TokenType == scanner.CONST {
		max, _ := p.Tokens.NextToken().Literal.(int)
		p.Tokens.PopToken()
		return LimitsNode{Min: min, Max: &max}
	} else {
		return LimitsNode{Min: min, Max: nil}
	}

}

// checkKeyword checks if the next token is of the specified type.
func (p *Parser) checkKeyword(tokenType int) bool {
	if p.Tokens.NextToken().TokenType == tokenType {
		p.Tokens.PopToken()
		return true
	}
	return false
}

// checkOpenParentheses checks if the next token is an open parenthesis.
func (p *Parser) checkOpenParentheses() bool {
	if p.Tokens.NextToken().TokenType == scanner.LPAREN {
		p.Tokens.PopToken()
		return true
	}
	return false
}

// checkClosingParentheses checks if the next token is a closing parenthesis.
func (p *Parser) checkCloseParentheses() bool {
	if p.Tokens.NextToken().TokenType == scanner.RPAREN {
		p.Tokens.PopToken()
		return true
	}
	return false
}

/* 
	checkOpenParentheses checks if the next token is an open parenthesis and the nextnext token is the specified keyword.
	We only pop the two tokens if both of these conditions are satisfied. If at least one is not satisfied then we do not
	pop any, as opposed to checking for an opening parentheses and keyword separately, which does not satisfy this statement.
*/
func (p *Parser) checkOpenParenthesesKeyword(keyordtype int) bool {
	if p.Tokens.NextToken().TokenType == scanner.LPAREN && p.Tokens.NextNextToken().TokenType == keyordtype {
		p.Tokens.PopToken()
		p.Tokens.PopToken()
		return true
	}
	return false
} 