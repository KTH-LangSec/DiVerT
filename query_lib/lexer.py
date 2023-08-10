import query_lib.token as token 

class Lexer:
    def __init__(self, _input):
        self.input = _input
        self.curr_pos = 0
        self.next_pos = 0
        self.ch = ""
        self.read_char()

    #######
    def read_char(self):
        if (self.next_pos >= len(self.input)):
            self.ch = ""
        else:
            self.ch = self.input[self.next_pos]

        self.curr_pos = self.next_pos
        self.next_pos += 1

    #######
    def skip_white_spaces(self):
        while (self.ch == " " or self.ch == "\t" or self.ch == "\n" or self.ch == "\r"):
            self.read_char()

    #######
    def read_identifier(self):
        _position = self.curr_pos
        _result = ""
        while (self.ch.isalpha() or self.ch.isnumeric() or self.ch == "_"):
            _result += self.ch
            self.read_char()

        return _result

    #######
    def read_string(self):
        self.read_char()
        _position = self.curr_pos
        _result = ""
        while (self.ch != "'"):
            _result += self.ch
            self.read_char()

        return _result

    #######
    def read_number(self):
        _position = self.curr_pos
        _result = ""
        while (self.ch.isnumeric()):
            _result += self.ch
            self.read_char()

        return _result

    #######
    def peek_char(self):
        if (self.next_pos >= len(self.input)):
            return ""
        else:
            return self.input[self.next_pos]

    #######
    def next_token(self):
        self.skip_white_spaces()

        match self.ch:
            case "'":
                string = self.read_string()
                tok = token.Token(token.STR, string)
            case "(":
                tok = token.Token(token.LPAREN, self.ch)
            case ")":
                tok = token.Token(token.RPAREN, self.ch)
            case "=":
                tok = token.Token(token.EQ, self.ch)
            case "+":
                tok = token.Token(token.PLUS, self.ch)
            case "-":
                tok = token.Token(token.MINUS, self.ch)
            case "!":
                if (self.peek_char() == "="):
                    _ch = self.ch
                    self.read_char()
                    tok = token.Token(token.NOT_EQ, _ch + self.ch)
                else:
                    tok = token.Token(token.BANG, self.ch)
            case "/":
                tok = token.Token(token.SLASH, self.ch)
            case "*":
                tok = token.Token(token.ASTERISK, self.ch)
            case "<":
                tok = token.Token(token.LT, self.ch)
            case ">":
                tok = token.Token(token.GT, self.ch)
            case ";":
                tok = token.Token(token.SEMICOLON, self.ch)
            case ",":
                tok = token.Token(token.COMMA, self.ch)
            case "":
                tok = token.Token(token.EOF, "")
            case _:
                if (self.ch.isalpha()):
                    _literal = self.read_identifier()
                    tok = token.Token(token.lookup_ident(_literal), _literal)
                    return tok
                elif (self.ch.isnumeric()):
                    _literal = self.read_number()
                    tok = token.Token(token.INT, _literal)
                    return tok
                else:
                    tok = token.Token(token.ILLEGAL, self.ch)
                    return tok

        self.read_char()
        return tok

    ####### Just a test method for tokenizing all the source code
    def tokenize(self):
        token_list = []
        curr_token = self.next_token()
        token_list.append(curr_token)
        while (curr_token.token_type != token.EOF):
            curr_token = self.next_token()
            token_list.append(curr_token)
        
        return token_list
