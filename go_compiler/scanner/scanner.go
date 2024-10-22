package scanner

import (
	"strconv"
)

// Define Deterministic Finite Automata for our tokens, with a dictionary as the transition function
type DFA struct {
	startState []string
	acceptingState []string
	transitionFunction map[string]string
}

// Define Deterministic Finite Automata for our tokens, with an array as the transition function
type DFAArrayTransition struct {
	startState []string
	acceptingState []string
	transitionFunction []string
}

// Define our token type
type Token struct {
	TokenText string
	Line int
	TokenType int // tokenType is an abstract type for our AST and interpreter
	Literal interface{} // The empty interface allows our literal to be **of any type**
}

// Define the methods for our TokenStream
type TokenStreamInterface interface {
	reset() 
	NextToken() Token
	NextNextToken() Token
	PopToken()
	HasNext() bool
	HasNextNext() bool
}

// Define our token stream
type TokenStream struct {
	Tokens []Token
	Next   int
}

// Reset the index for our token stream
func (t *TokenStream) reset() {
	t.Next = 0
}

// Return the next token in our token stream. 
// If it is null return a null reference; otherwise return 
// the address of the referenced token
func (t *TokenStream) NextToken() *Token {
	if !t.HasNext() {
		return nil
	} 
	return &t.Tokens[t.Next]
}

// Return the next next token in our token stream. 
// If it is null return a null reference; otherwise return 
// the address of the referenced token
func (t *TokenStream) NextNextToken() Token {
	if !t.HasNextNext() {
		return Token{}
	} 
	return t.Tokens[t.Next+1]
}

// Pop the token from the token stream
func (t *TokenStream) PopToken() {
	t.Next += 1
}

// Check to see if the token stream has a next value
func (t *TokenStream) HasNext() bool {
	return t.Next < len(t.Tokens)
}

// Check to see if the token stream has a next next value
func (t *TokenStream) HasNextNext() bool {
	return t.Next+1 < len(t.Tokens)
}

// Scanner Interface stores our methods for our scanner struct
type ScannerInterface interface {
	Advance(inc int)
	isAtEnd() bool
	current() string
	next() string
	scanToken() TokenStream
}

// Scanner struct allows us to tokenize a source file
type Scanner struct {
	CurrentIndex int
	Source string
    Line int
    Tokens []Token
}

// Increment the current index in the source file
func (s *Scanner) advance(increment int) int {
	s.CurrentIndex += increment
	return s.CurrentIndex
} 

// Check to see if we are at the end of the source file
func (s *Scanner) isAtEnd() bool {
	return (s.CurrentIndex >= len(s.Source))
} 

// Get the current character in the source file
func (s *Scanner) current() string {
	return string(s.Source[s.CurrentIndex])
} 

// Get the next character in the source file
func (s *Scanner) next() string {
	return string(s.Source[s.CurrentIndex+1])
} 

// Scan the tokens and return a TokenStream
func (s *Scanner) ScanTokens() TokenStream {

	// Define string DFA
	stringDFA := new(DFA)
	stringDFA.startState = []string{"\""}
	stringDFA.acceptingState = []string{"\""}

	// String transition function
	stringMap := map[string]string{
		"\\":  "\"",
	}
	stringDFA.transitionFunction = stringMap

	// Define line comment DFA
	lineCommentDFA := new(DFA)
	lineCommentDFA.startState = []string{";",";"}
	lineCommentDFA.acceptingState = []string{"\n"}

	// Define block comment DFA
	blockCommentDFA := new(DFA)
	blockCommentDFA.startState = []string{"(",";"}
	blockCommentDFA.acceptingState =[]string{";",")"}

	// Define keyword DFA
	keywordDFA := new(DFAArrayTransition)
	keywordDFA.startState = []string{"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
		"n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}
	
	keywordDFA.transitionFunction = []string{
		"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
		"n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
		"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
		"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
		"!", "#", "$", "%", "&", "*", "-", "+", ".", "/", ":", "<", "`",
		"=", ">", "?", "@", "\\", "^", "'", "_", "|", "~", "0", "1", "2",
		"3", "4", "5", "6", "7", "8", "9",
	}

	// Define integer DFA
	integerDFA := new(DFAArrayTransition)
	integerDFA.startState = []string{"+", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

	integerDFA.transitionFunction =  []string{"_", "0", "1", "2",
	"3", "4", "5", "6", "7", "8", "9"}

	// Define ID DFA
	idDFA := new(DFAArrayTransition)
	idDFA.startState = []string{"$"}
	
	idDFA.transitionFunction =  []string{
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "!", "#", "$", "%", "&", "", "*", "-", "+", ".", "/", ":", "<", 
    "=", ">", "?", "@", "\\", "^", "'", "_", "|", "~", "0", "1", "2",
    "3", "4", "5", "6", "7", "8", "9",
	}
	

	for !s.isAtEnd() {
		// Block comment scan
		if s.current() == blockCommentDFA.startState[0] && s.next() == blockCommentDFA.startState[1] {
			s.advance(2)
			for s.current() != blockCommentDFA.acceptingState[0] && s.next() != blockCommentDFA.acceptingState[1] { 
				s.advance(1)
			}
			s.advance(2)

		} else if s.current() == lineCommentDFA.startState[0] && s.next() == lineCommentDFA.startState[1] { // Line comment scan
			s.advance(2)
			for s.current() != lineCommentDFA.acceptingState[0] {
				s.advance(1)
			}

		} else if s.current() == stringDFA.startState[0] { // String scan
			s.advance(1)
			startIndex := s.CurrentIndex
			// i.e., while the current token is not at an accepting state
			for s.current() != stringDFA.acceptingState[0] {
				// Check to see if our current character is a key in our transition function
				if containsMap(stringDFA.transitionFunction,s.current()) {
					// If it is, then we expect a certain token
					if s.next() != stringDFA.transitionFunction[s.current()] {
						return TokenStream{Tokens: []Token{}, Next: 0}
					}
					s.advance(1)
				} 
				s.advance(1)
			}
			// Exit out of the ending ' " ' character
			s.advance(1)
			// Get the literal of the string that was parsed
			literal := s.Source[startIndex:s.CurrentIndex-1]
			// Create new token object
			token := new(Token)
			token.TokenText = literal
			token.Line = s.Line
			token.TokenType = STR
			token.Literal = literal
			// Add token object to our list of tokens
			s.Tokens = append(s.Tokens, *token)
			
		} else if s.current() == "(" { // Left parentheses scan
			s.advance(1)
			// Create new token object
			token := new(Token)
			token.TokenText = "("
			token.Line = s.Line
			token.TokenType = LPAREN
			token.Literal = "("
			// Add the token object to our list of tokens
			s.Tokens = append(s.Tokens, *token)
			
		} else if s.current() == ")" { // Right parentheses scan
			s.advance(1)
			// Create new token object
			token := new(Token)
			token.TokenText = ")"
			token.Line = s.Line
			token.TokenType = RPAREN
			token.Literal = ")"
			// Add the token object to our list of tokens
			s.Tokens = append(s.Tokens, *token)

		} else if s.current() == "\n" { // Whitespace scan
			s.Line += 1
			s.advance(1)

		} else if s.current() == "\r" || s.current() == " " { // Whitespace scan
			s.advance(1)

		} else if containsArray(keywordDFA.startState, s.current()) { // Keyword scan
			startIndex := s.CurrentIndex
			s.advance(1)
			for containsArray(keywordDFA.transitionFunction, s.current()) {
				s.advance(1)
			}
			// Get the literal of the string that was parsed
			literal := s.Source[startIndex:s.CurrentIndex]

			var tokenType *int = nil
			
			// Loop through token names and find the corresponding 
			// abstract type
			for i, str := range tokenNames {
				if str == literal {
					tokenType = &i
					break
				}
			}
			
			// Create new token object
			token := new(Token)
			token.TokenText = literal
			token.Line = s.Line
			token.TokenType = *tokenType
			token.Literal = literal
			// Add token object to our list of Tokens
			s.Tokens = append(s.Tokens, *token)
		} else if containsArray(integerDFA.startState, s.current()) { // Integer scan
			startIndex := s.CurrentIndex
			s.advance(1)
			for containsArray(integerDFA.transitionFunction, s.current()) {
				s.advance(1)
			}
			literal := s.Source[startIndex:s.CurrentIndex]
			tokenType := CONST
			token := new(Token)
			token.TokenText = literal
			token.Line = s.Line
			token.TokenType = tokenType
			token.Literal, _ = strconv.Atoi(literal)
			s.Tokens = append(s.Tokens, *token)

		} else if containsArray(idDFA.startState, s.current()) { // Identifier scan
			startIndex := s.CurrentIndex
			s.advance(1)
			for containsArray(idDFA.transitionFunction, s.current()) {
				s.advance(1)
			}
			token := new(Token)
			token.TokenText = s.Source[startIndex:s.CurrentIndex]
			token.Line = s.Line
			token.TokenType = IDENTIFIER
			token.Literal =  s.Source[startIndex:s.CurrentIndex]
			s.Tokens = append(s.Tokens, *token)
		}

	}
	token := new(Token)
	token.TokenText = ""
	token.Line = s.Line
	token.TokenType = EOF
	s.Tokens = append(s.Tokens, *token)
	Tokenstream := new(TokenStream)
	Tokenstream.Tokens = s.Tokens
	return *Tokenstream

}


// Function to check if a string exists in a map. 
// Source: https://stackoverflow.com/questions/2050391/how-to-check-if-a-map-contains-a-key-in-go
func containsMap(m map[string]string, key string) bool {
	// `val` is the value of m[key]; `ok` is a bool that will be set to true
	// if the key exists
	_, keyExists := m[key]
	return keyExists
}

func containsArray(arr []string, key string) bool {
	for _, value := range arr {
		if value == key {
			return true
		}
	}
	return false
}
