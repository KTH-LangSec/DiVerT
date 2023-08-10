import parser_lib.token as token
import parser_lib.ast as ast
import parser_lib.expression as expression
import parser_lib.macro as macro
import sys


class Parser:
    def __init__(self, _lexer):
        self.lexer = _lexer

        self.curr_token = token.Token(token.ILLEGAL, "")
        self.peek_token = token.Token(token.ILLEGAL, "")

        # Read two tokens, so curr_token and peek_token are both set
        self.next_token()
        self.next_token()

    #######
    def next_token(self):
        self.curr_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    #######
    def parse_program(self):
        stm_list = []
        table_defs = {}
        policy_defs = []

        while (self.curr_token.token_type != token.EOF):
            if (self.curr_token.token_type == token.POLICY):
                policy_defs = self.curr_token
            elif (self.curr_token.token_type == token.TABLE):
                for key, value in self.curr_token.literal.items(): 
                    table_defs[key] = value
            else:
                stm_node = self.parse_statement()
                if (stm_node != None):
                    stm_list.append(stm_node)
            
            self.next_token()

        return {"stm_list": stm_list, "table_defs":table_defs, "policy_defs":policy_defs}

    #######
    def parse_statement(self):
        match self.curr_token.token_type:
            case token.IF:
                return self.parse_if()
            case token.WHILE:
                return self.parse_while()
            case token.OUT:
                return self.parse_output()
            case token.IDENT:
                return self.parse_assignment()
            case token.SKIP:
                return self.parse_skip()
            case _:
                return None

    #######
    def parse_assignment(self):
        idnt_token = self.curr_token

        if (not self.expect_peek(token.ASSIGN)):
            return None
        
        self.next_token() # to skip =

        exp_lst = []
        while (not self.curr_token_is(token.SEMICOLON)):
            if (self.curr_token_is(token.EOF) or self.curr_token_is(token.ASSIGN)):
                print(">>> PARSE ERORR: Expected semicolon.")
                sys.exit(0)
            
            exp_lst.append(self.curr_token)
            self.next_token()

        exp = expression.Expression(exp_lst)
        stm_node = ast.AssignNode(idnt_token, exp)

        return stm_node

    #######
    def parse_output(self):
        if (not self.expect_peek(token.LPAREN)):
            return None
        
        self.next_token() # to skip (

        exp_lst = []
        while (not self.curr_token_is(token.COMMA)):
            exp_lst.append(self.curr_token)
            self.next_token()

        if (not self.expect_peek(token.IDENT)):
            return None
        # curr_token is user variable

        exp = expression.Expression(exp_lst)
        stm_node = ast.OutNode(exp, self.curr_token)

        # Skip eveything else until semicolon
        while (not self.curr_token_is(token.SEMICOLON)):
            self.next_token()

        return stm_node

    #######
    def parse_while(self):
        self.next_token()

        exp_lst = []
        while (not self.curr_token_is(token.DO)):
            exp_lst.append(self.curr_token)
            self.next_token()

        if (not self.expect_peek(token.LBRACE)):
            return None
        # curr_token is {

        body_stm_list = []
        while (not self.curr_token_is(token.RBRACE)):
            body_stm_node = self.parse_statement()
            if (body_stm_node != None):
                body_stm_list.append(body_stm_node)
            
            self.next_token()

        exp = expression.Expression(exp_lst)
        stm_node = ast.WhileNode(exp, body_stm_list)

        return stm_node

    #######
    def parse_if(self):
        self.next_token()

        exp_lst = []
        while (not self.curr_token_is(token.THEN)):
            exp_lst.append(self.curr_token)
            self.next_token()

        if (not self.expect_peek(token.LBRACE)):
            return None
        # curr_token is {

        then_stm_list = []
        while (not self.curr_token_is(token.RBRACE)):
            then_stm_node = self.parse_statement()
            if (then_stm_node != None):
                then_stm_list.append(then_stm_node)
            
            self.next_token()

        ## TODO for now we always expect ELSE
        if (not self.expect_peek(token.ELSE)):
            return None
        if (not self.expect_peek(token.LBRACE)):
            return None
        # curr_token is {

        else_stm_list = []
        while (not self.curr_token_is(token.RBRACE)):
            else_stm_node = self.parse_statement()
            if (else_stm_node != None):
                else_stm_list.append(else_stm_node)
            
            self.next_token()

        exp = expression.Expression(exp_lst)
        stm_node = ast.IfNode(exp, then_stm_list, else_stm_list)

        return stm_node

    #######
    def parse_skip(self):
        if (not self.expect_peek(token.SEMICOLON)):
            return None

        stm_node = ast.SkipNode()

        return stm_node


    #######
    def expect_peek(self, type):
        if self.peek_token_is(type):
            self.next_token()
            return True
        else:
            self.peek_error(type)
            return False

    def curr_token_is(self, type):
        return self.curr_token.token_type == type
    
    def peek_token_is(self, type):
        return self.peek_token.token_type == type

    def peek_error(self, type):
        print(">>> PARSE ERORR: expected next token to be "+ str(type) +", got "+ str(self.peek_token.token_type) +" instead")

