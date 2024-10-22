#include <iostream> 
#include <string> // for string class 

using namespace std; 


#include <string>
#include <vector>

// Create our token names for our parser
enum Token {
    I32 = 0,
    F32,
    I64,
    F64,
    FUNCREF,
    EXTERNREF,
    FUNC,
    EXTERN,
    CONST,       // No explicit keyword, used for literals
    STR,         // No explicit keyword, used for literals
    LOCAL,
    PARAM,
    CALL,
    IMPORT,
    EXPORT,
    TABLE,
    MEMORY,
    GLOBAL,
    TYPE,
    LOCAL_GET,
    LOCAL_SET,
    LOCAL_TEE,
    GLOBAL_GET,
    GLOBAL_SET,
    IF,
    END,
    ELSE,
    CALL_INDIRECT,
    BR,
    BR_IF,
    RETURN,
    BLOCK,
    LOOP,
    MUT,
    IDENTIFIER,
    I32_ADD,
    I32_CONST,
    I32_GT_U
};

// Create an implicit mapping between the abstract token name and the literal terminal
std::vector<std::string> tokenNames = {
    "i32",
    "f32",
    "i64",
    "f64",
    "funcref",
    "externref",
    "func",
    "extern",
    "",      // Const terminal is not constricted to a specific keyword
    "",      // String terminal is not constricted to a specific keyword
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
    "i32.const",
    "i32.gt_u"
};


struct {
	string attribute;
	int line;
	int tokenType;

} token;