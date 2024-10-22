# Those KVPAIRS with a None entry are considered nonterminals 
LPAREN, RPAREN, STR, INT, EOF, ID, MODULEFIELD, FUNC, GLOBAL, GET, OFFSET, GE_S, STORE, CALL_INDIRECT, BR, MEMORY, CALL, AND, TYPE, BR_IF, LOAD, SUB, RETURN, CONST, LOCAL, RESULT, MODULE, ALIGN, EXPORT, DROP, TEE, ADD, EQ, OR, EQZ, SET, LOOP, PARAM, END, EXTEND_I32_S, MUT, TABLE, LT_S, FUNCREF, VECTYPE, REFTYPE, EXTERNREF, I32, I64, F32, F64, BLOCK, BLOCKTYPE, IF, ELSE, IMPORT, GT_U = range(57)
KVPAIRS = ['(', ')', None, None, None, None, None, 'func', 'global', 'get', 'offset', 'ge_s', 'store', 'call_indirect', 'br', 'memory', 'call', 'and', 'type', 'br_if', 'load', 'sub', 'return', 'const', 'local', 'result', 'module', 'align', 'export', 'drop', 'tee', 'add', 'eq', 'or', 'eqz', 'set', 'loop', 'param', 'end', 'extend_i32_s', 'mut', 'table', 'lt_s', 'funcref', 'v128', None, 'externref', 'i32', 'i64', 'f32', 'f64', 'block', None, 'if', 'else', 'import', 'gt_u']


INSTRUCTION = 1489393
LIMITS = 100000
NAME = 100001
TABLETYPE = 100002
GLOBALTYPE = 100003
FUNCTYPE = 100004
MEMORYUSE = 1000005
TYPEUSE = 1000007
MEMARG = 1000008
IF = 1000012
ELSE = 1000009
GLOBALGET = 100045009
GLOBALSET = 103045009
GLOBALTEE = 102045009
LOCALGET = 120045009
LOCALSET = 153045009
LOCALTEE = 162045009
STRCTCNTRLINSTR = 162045309
I32CONST = 162045339
I64CONST = 162745309
F32CONST = 162034309
F64CONST = 162022309
LABEL = 162026309
