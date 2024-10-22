package parser

type LocalNode struct {
	TokenType int
	Identifier interface{}
	Value int
}

type ReturnNode struct {
	TokenType int
}
type ModuleNode struct {
	Id interface{};
	ModuleFields []interface{}
	Env Env
}

type ImportNode struct {
	ModuleName string
	Name string
	ImportDescendant interface{}
}

type FuncNode struct {
	Id int
	TypeIndex int
	Frame *Frame
	Instructions []interface{} // InstructionNode or StructuredControlInstruction nodes
}

type InstructionNode struct {
	TokenType int
	Operand interface{}
}

type StructuredInstructionNode struct {
	TokenType int
	Instructions []interface{} // InstructionNode or StructuredControlInstruction nodes
	Index int
}

type FunctypeNode struct {
	Id int
}

type TypeuseNode struct {
	Identifier int
	Frame *Frame

}


type MemoryNode struct {
	Identifier int
	ValType LimitsNode

}

type ExportNode struct {
	Name string
	Id int
}

type LimitsNode struct {
	Min int
	Max *int // max may be empty
}