#include <vector>


using namespace std;

// shorthand for our abstract token name enum
typedef int valType; 

typedef struct param {
    std::optional<string> identifier;
    valType valtype;
};

typedef struct local {
    std::optional<string> identifier;
    valType valtype;
};

typedef struct typeIdentifier {
    std::optional<string> identifier;
    funcType functype;
};

struct funcType {
    vector<valType> params;
    vector<valType> results;
};
 
typedef struct limits {
    int min;
    std::optional<int> max;
};

typedef struct instruction {
    valType type;
    std::optional<int> operand;
};

typedef struct tableType {
    limits lim;
    valType reftype;
};

typedef struct globalType {
    int type; // var or const
    valType valtype;
};

typedef struct blockInstr {
    union blockType {
        optional<valType> result;
        int typeIdx;
    };
    vector<instruction> instrs;
};

typedef struct function {
    std::optional<string> identifier;
    int typeIdx;
    vector<local> locals;
    vector<instruction> instrs;
};