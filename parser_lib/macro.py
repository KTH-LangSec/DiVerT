import parser_lib.token as Ptoken
import query_lib.token as Qtoken


def tokenize(_input):
    parts = _input[:-1].split("(")
    match parts[0].lower():
        case "table":
            return analyze_table(_input[6:-1])
        case "policy":
            return analyze_policy(_input[7:-1])
        case "query":
            return analyze_query(_input[6:-1])
        case _:
            return Ptoken.ILLEGAL


def analyze_query(_query):
    return Ptoken.Token(Ptoken.QUERY, _query)

def analyze_table(_table):
    tableDef = {}
    parts = _table.split(",")

    table_name = parts[0].strip()
    columnsDef = {}
    for i in range(1,len(parts)):
        tmp = parts[i].strip().split(":")
        match (tmp[1].strip().lower()):
            case "str":
                columnsDef[tmp[0].strip()] = Qtoken.STR
            case "string":
                columnsDef[tmp[0].strip()] = Qtoken.STR
            case "int":
                columnsDef[tmp[0].strip()] = Qtoken.INT
            case "integer":
                columnsDef[tmp[0].strip()] = Qtoken.INT
            case "bool":
                columnsDef[tmp[0].strip()] = Qtoken.BOOL
            case "boolean":
                columnsDef[tmp[0].strip()] = Qtoken.BOOL
            case _:
                columnsDef[tmp[0].strip()] = Qtoken.ILLEGAL


    tableDef[table_name] = columnsDef

    return Ptoken.Token(Ptoken.TABLE, tableDef)

def analyze_policy(_policy):
    disjunctions = []

    for part in _policy.split("|"):
        conjunctions = []
        splitted_con = part.strip().split(";")
        for c in splitted_con:
            if c.strip():
                conjunctions.append(c.strip()+";")
        
        disjunctions.append(conjunctions)

    return Ptoken.Token(Ptoken.POLICY, disjunctions)