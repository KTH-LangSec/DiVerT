####### CONSTANTS #######
# Specials
ILLEGAL = "ILLEGAL"
EOF = "EOF"
# Marcro Tokens
QUERY = "QUERY"
TABLE = "TABLE"
POLICY = "POLICY"
# Identifiers + literals
IDENT = "IDENT" # add, foobar, x, y, ...
INT   = "INT"   # 1343456
STR = "STR"
# Operators
ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"
LT = "<"
GT = ">"
EQ = "=="
NOT_EQ = "!="
# Delimiters
COMMA = ","
SEMICOLON = ";"
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"
# Keywords
OUT = "OUT"
WHILE = "WHILE"
DO = "DO"
IF = "IF"
ELSE = "ELSE"
THEN = "THEN"
SKIP = "SKIP"
TRUE = "TRUE"
FALSE = "FALSE"


class Token:
    def __init__(self, _token_type, _literal):
        self.token_type = _token_type
        self.literal = _literal

    def __str__(self):
        if (self.token_type == QUERY):
            return "Query<<"+self.literal+">>"
        else:
            #return str("Token of type " + self.token_type + " with literal " + self.literal)
            return str(self.literal)
    
    def __repr__(self):
        return str(self)

def lookup_ident(_literal):
    match _literal.lower():
        case "out":
            return OUT
        case "while":
            return WHILE
        case "do":
            return DO
        case "if":
            return IF
        case "then":
            return THEN
        case "else":
            return ELSE
        case "skip":
            return SKIP
        case "false":
            return FALSE
        case "true":
            return TRUE
        case _:
            return IDENT
