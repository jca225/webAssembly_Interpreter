
// Create our token names for our parser
const (
	I32          = iota
	F32          = iota
	I64          = iota
	F64          = iota
	FUNCREF      = iota
	EXTERNREF    = iota
	FUNC         = iota
	EXTERN       = iota
	CONST        = iota
	STR          = iota
	LOCAL        = iota
	PARAM        = iota
	CALL         = iota
	IMPORT       = iota
	EXPORT       = iota
	TABLE        = iota
	MEMORY       = iota
	GLOBAL       = iota
	TYPE         = iota
	LOCAL_GET    = iota
	LOCAL_SET    = iota
	LOCAL_TEE    = iota
	GLOBAL_GET   = iota
	GLOBAL_SET   = iota
	IF           = iota
	END          = iota
	ELSE         = iota
	CALL         = iota
	CALL_INDIRECT= iota
	BR           = iota
	BR_IF        = iota
	RETURN       = iota
	BLOCK        = iota
	LOOP         = iota
	MUT          = iota
	IDENTIFIER   = iota
	I32_ADD      = iota
	I32_CONST    = iota
	I32_GT_U     = iota

)

// Create an implicit mapping between the abstract token name and the literal terminal
var tokenNames = []string{
	"i32",
	"f32",
	"i64",
	"f64",
	"funcref",
	"externref",
	"func",
	"extern",
	nil, // Const terminal is not constricted to a specific keyword
	nil, // String terminal is not constricted to a specific keyword
	"local",
	"param",
	"call",
	"import",
	"export",
	"table",
	"memory",
	"global",
	"type",
	"local.get",
	"local.set",
	"local.tee",
	"global.get",
	"global.set",
	"if",
	"end",
	"else",
	"call",
	"call_indirect",
	"br",
	"br_if",
	"return",
	"block",
	"loop",
	"mut",
	"identifier",
	"i32.add",
	"i32.const",
	"i32.gt_u",
}

// Define a type that will hold our tokens for parsing
type token struct {
	attribute str
	line int
	tokenType int

}

