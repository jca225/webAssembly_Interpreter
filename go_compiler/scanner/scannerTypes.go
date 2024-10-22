package scanner


// Create our token names for our parser
const (
	MODULE        = iota
	I32           = iota
	F32           = iota
	I64           = iota
	F64           = iota
	FUNCREF       = iota
	EXTERNREF     = iota
	FUNC          = iota
	EXTERN        = iota
	CONST         = iota
	STR           = iota
	LOCAL         = iota
	PARAM         = iota
	CALL          = iota
	IMPORT        = iota
	EXPORT        = iota
	TABLE         = iota
	MEMORY        = iota
	GLOBAL        = iota
	TYPE          = iota
	LOCAL_GET     = iota
	LOCAL_SET     = iota
	LOCAL_TEE     = iota
	GLOBAL_GET    = iota
	GLOBAL_SET    = iota
	IF            = iota
	END           = iota
	ELSE          = iota
	CALL_INDIRECT = iota
	BR            = iota
	BR_IF         = iota
	RETURN        = iota
	BLOCK         = iota
	LOOP          = iota
	MUT           = iota
	IDENTIFIER    = iota
	I32_ADD       = iota
	I32_GT_U      = iota
	RPAREN        = iota 
	LPAREN        = iota
	EOF           = iota
	I32_CONST     = iota
	I64_CONST     = iota
	F32_CONST     = iota
	F64_CONST     = iota
	RESULT        = iota
	GE_S          = iota
)

// Create an implicit mapping between the abstract token name and the literal terminal
var tokenNames = []string{
	"module",
	"i32",
	"f32",
	"i64",
	"f64",
	"funcref",
	"externref",
	"func",
	"extern",
	"", // Const terminal is not constricted to a specific keyword
	"", // String terminal is not constricted to a specific keyword
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
	"call_indirect",
	"br",
	"br_if",
	"return",
	"block",
	"loop",
	"mut",
	"identifier",
	"i32.add",
	"i32.gt_u",
	"(",
	")",
	"", // EOF is an abstract type with no definitive value associated with it
	"i32.const",
	"i64.const",
	"f32.const",
	"f64.const",
	"result",
	"i32.ge_s",
}