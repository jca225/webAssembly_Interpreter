OPEN_PAREN, CLOSE_PAREN, IDENTIFIER, MODULE, NAME, FUNC, NUMERIC, STRING, NUMTYPE, INSTR, EOF, EXPORT, IMPORT, PARAM, RESULT, MODULEFIELD, LOCAL = range(17)

WHITESPACETOKENS = ['\n', '\r', '\r\n', ' ']

TERMINALTOKENS = WHITESPACETOKENS + [')']

NUMTYPES = ['i32', 'i64', 'f32', 'f64']

VECTOKENS = ['v128', 'i8x16', 'i16x8', 'i32x4', 'i64x2', 'f32x4', 'f64x2']

REFTYPES = ['funcref', 'externref']

HEAPTYPES = ['func', 'extern']

FUNCTYPES = ['func', 'param', 'result']

VALUETYPES = NUMTYPES + REFTYPES + ['v128']

BLOCKTOKENS = ['block', 'loop', 'if', 'else', 'end']

CONTROLTOKENS = ['unreachable', 'nop', 'br', 'br_if', 'br_table', 'return', 'call', 'call_indirect']

REFTOKENS = ['ref.null', 'ref.is_null', 'ref.func']

PARAMTOKENS = ['drop', 'select']

VARTOKENS = ['local.get', 'local.set', 'local.tee',  'global.get', 'global.set']

TABTOKENS = ['table.get', 'table.set', 'table.size', 'table.grow', 'table.fill', 'table.copy', 'table.init', 'elem.drop']

MEMTOKENS = ['offset', 'align', 'memory.size', 'memory.grow', 'memory.copy', 'memory.init', 'data.drop']


NUMTOKENS = []
for numtype in NUMTYPES:
    NUMTOKENS.append(numtype + '.const')
    MEMTOKENS.append(numtype + '.load')
    MEMTOKENS.append(numtype + '.store')
    if (numtype == 'i32' or numtype == 'i64'):
        MEMTOKENS.append(numtype + '.load8_s')
        MEMTOKENS.append(numtype + '.load8_u')
        MEMTOKENS.append(numtype + '.load16_s')
        MEMTOKENS.append(numtype + '.load16_u')
        MEMTOKENS.append(numtype + '.store_8')
        MEMTOKENS.append(numtype + '.store_16')

        NUMTOKENS.append(numtype + '.clz')
        NUMTOKENS.append(numtype + '.ctz')
        NUMTOKENS.append(numtype + '.popcnt')
        NUMTOKENS.append(numtype + '.add')
        NUMTOKENS.append(numtype + '.sub')
        NUMTOKENS.append(numtype + '.mult')
        NUMTOKENS.append(numtype + '.div_s')
        NUMTOKENS.append(numtype + '.div_u')
        NUMTOKENS.append(numtype + '.rem_s')
        NUMTOKENS.append(numtype + '.rem_u')
        NUMTOKENS.append(numtype + '.and')
        NUMTOKENS.append(numtype + '.or')
        NUMTOKENS.append(numtype + '.xor')
        NUMTOKENS.append(numtype + '.shl')
        NUMTOKENS.append(numtype + '.shr_s')
        NUMTOKENS.append(numtype + '.shr_u')
        NUMTOKENS.append(numtype + '.rotl')
        NUMTOKENS.append(numtype + '.rotr')
        NUMTOKENS.append(numtype + '.div_u')
        NUMTOKENS.append(numtype + '.rem_s')
        NUMTOKENS.append(numtype + '.rem_u')

        NUMTOKENS.append(numtype + '.eqz')
        NUMTOKENS.append(numtype + '.eq')
        NUMTOKENS.append(numtype + '.ne')
        NUMTOKENS.append(numtype + '.lt_s')
        NUMTOKENS.append(numtype + '.lt_u')
        NUMTOKENS.append(numtype + '.gt_s')
        NUMTOKENS.append(numtype + '.gt_u')
        NUMTOKENS.append(numtype + '.le_s')
        NUMTOKENS.append(numtype + '.le_u')
        NUMTOKENS.append(numtype + '.ge_s')
        NUMTOKENS.append(numtype + '.ge_u')

        NUMTOKENS.append(numtype + '.trunc_f32_s')
        NUMTOKENS.append(numtype + '.trunc_f32_u')
        NUMTOKENS.append(numtype + '.trunc_f64_s')
        NUMTOKENS.append(numtype + '.trunc_f64_u')
        NUMTOKENS.append(numtype + '.trunc_sat_f32_u')
        NUMTOKENS.append(numtype + '.trunc_sat_f32_s')
        NUMTOKENS.append(numtype + '.trunc_sat_f64_u')
        NUMTOKENS.append(numtype + '.trunc_sat_f64_s')

        MEMTOKENS.append(numtype + '.extend8_s')
        MEMTOKENS.append(numtype + '.extend16_s')


    if (numtype == 'i32'):
        NUMTOKENS.append(numtype + '.wrap_i64')

        NUMTOKENS.append(numtype + '.reinterpret_f32')

    if (numtype == 'i64'):
        MEMTOKENS.append(numtype + '.load32_s')
        MEMTOKENS.append(numtype + '.load32_u')
        MEMTOKENS.append(numtype + '.store_32')
        NUMTOKENS.append(numtype + '.extend_i32_s')
        NUMTOKENS.append(numtype + '.extend_i32_u')

        NUMTOKENS.append(numtype + '.reinterpret_f64')

        NUMTOKENS.append(numtype + '.extend32_s')

    if (numtype == 'f32' or numtype == 'f64'):
        NUMTOKENS.append(numtype + '.abs')
        NUMTOKENS.append(numtype + '.neg')
        NUMTOKENS.append(numtype + '.ceil')
        NUMTOKENS.append(numtype + '.floor')
        NUMTOKENS.append(numtype + '.trunc')
        NUMTOKENS.append(numtype + '.nearest')
        NUMTOKENS.append(numtype + '.sqrt')
        NUMTOKENS.append(numtype + '.add')
        NUMTOKENS.append(numtype + '.sub')
        NUMTOKENS.append(numtype + '.mul')
        NUMTOKENS.append(numtype + '.div')
        NUMTOKENS.append(numtype + '.min')
        NUMTOKENS.append(numtype + '.max')
        NUMTOKENS.append(numtype + '.copysign')

        NUMTOKENS.append(numtype + '.eq')
        NUMTOKENS.append(numtype + '.ne')
        NUMTOKENS.append(numtype + '.lt')
        NUMTOKENS.append(numtype + '.gt')
        NUMTOKENS.append(numtype + '.le')
        NUMTOKENS.append(numtype + '.ge')

        NUMTOKENS.append(numtype + '.convert_i32_s')
        NUMTOKENS.append(numtype + '.convert_i32_u')
        NUMTOKENS.append(numtype + '.convert_i64_s')
        NUMTOKENS.append(numtype + '.convert_i64_u')

    if numtype == 'f32':
        NUMTOKENS.append(numtype + '.demote_f64')

    if numtype == 'f64':
        NUMTOKENS.append(numtype + '.promote_f32')


ALLTOKENS = NUMTYPES + VECTOKENS + REFTYPES + HEAPTYPES + FUNCTYPES + BLOCKTOKENS + CONTROLTOKENS + REFTOKENS + PARAMTOKENS + VARTOKENS + TABTOKENS + MEMTOKENS + NUMTOKENS

INSTRUCTIONS = NUMTOKENS + MEMTOKENS
ALLTOKENS = sorted(ALLTOKENS, key=len)

SPECIALCHARS = ['!', '#', '$', '%', '&', '`', '*', '-', '+', '.', '/', ':', '<', '=', '>', '?', '@', '\\', '^', '\'', '_', '|', '~']

HEXKVPAIRS = {'A': 10, 
              'a': 10,
              'B': 11, 
              'b': 11,
              'C': 12, 
              'c': 12,
              'D': 13, 
              'd': 13,
              'E': 14, 
              'e': 14,
              'F': 15, 
              'f': 15,
}