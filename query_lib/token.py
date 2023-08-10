####### CONSTANTS #######
# Specials
ILLEGAL = "ILLEGAL"
EOF = "EOF"
# Identifiers + literals
IDENT = "IDENT" # add, foobar, x, y, ...
INT   = "INT"   # 1343456
STR   = "STR"   # test
BOOL = "BOOL"   # boolean
# Operators
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"
LT = "<"
GT = ">"
EQ = "="
NOT_EQ = "!="
# Delimiters
COMMA = ","
SEMICOLON = ";"
LPAREN = "("
RPAREN = ")"
# Keywords
SELECT = "SELECT"
FROM = "FROM"
WHERE = "WHERE"
AND = "AND"
TRUE = "TRUE"
FALSE = "FALSE"


class Token:
    def __init__(self, _token_type, _literal):
        self.token_type = _token_type
        self.literal = _literal

    def __str__(self):
        return str("Token of type " + self.token_type + " with literal " + self.literal)
        #return str(self.literal)
    
    def __repr__(self):
        return str(self)

def lookup_ident(_literal):
    match _literal.lower():
        case "select":
            return SELECT
        case "and":
            return AND
        case "where":
            return WHERE
        case "from":
            return FROM
        case "false":
            return FALSE
        case "true":
            return TRUE
        case _:
            return IDENT