
type functype struct {
	params: []param
	results: []result
}

type param struct {
	valtype: int
	id: *string // id can be empty
}

type local struct {
	valtype: int
	id: *string // id can be empty
}

type importType struct {
	module: string
	name: string
	descendant: // can be func, table, memory, or global
}

type result struct {
	valtype: int
}

type Func struct {
	typeuse 
	locals []local
}

type id struct {
	id *string // id can be empty
}

type limits struct {
	min uint32
	max *uint32 // max can be empty
}

type tabletype struct {
	lim limits
	et int
}

type globaltype struct {
	valtype int
	constOrVar bool
}

type global struct {
	init // Initial expression
	globalType globaltype // reference to type
}

type typeuse struct {
	typeidx int
}

type Type struct {

}


type moduleType struct {
	
}