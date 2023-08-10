import query_lib.lexer as Qlexer
import query_lib.parser as Qparser

import label_lib.symbolic_tuple as st_lib
import label_lib.label as lb_lib


#################### generate a symbolic tuple for a query ####################
def get_symbolic_tuple(_sql):
    lx = Qlexer.Lexer(_sql)
    prs = Qparser.Parser(lx)
    parsed_query = prs.parse_select()

    return st_lib.SymbolicTuple(parsed_query[0], parsed_query[1], parsed_query[2])


#################### generate a label for a set of queries ####################
def get_label(_set_of_queries):
    label = lb_lib.Label()
    for q in _set_of_queries:
        label.add_st(get_symbolic_tuple(q))
    
    return label