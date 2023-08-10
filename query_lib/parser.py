import query_lib.token as token
import query_lib.expression as expression

import settings

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
    def parse_select(self):
        if (not self.expect_curr(token.SELECT)):
            return None

        projection_list = set()
        while (not self.curr_token_is(token.FROM)):
            if (self.curr_token_is(token.IDENT)):
                projection_list.add(self.curr_token.literal)

            if (self.curr_token_is(token.ASTERISK)):
                projection_list.add(self.curr_token.literal)

            self.next_token()

        table_list = set()
        while (not (self.curr_token_is(token.WHERE) or self.curr_token_is(token.SEMICOLON))):
            if (self.curr_token_is(token.IDENT)):
                table_list.add(self.curr_token.literal)

            self.next_token()

        expression_list = []
        if (not self.curr_token_is(token.SEMICOLON)):
            if (not self.expect_curr(token.WHERE)):
                return None
            
            temp_list = []
            while (not self.curr_token_is(token.SEMICOLON)):
                temp_list.append(self.curr_token)
                self.next_token()

            for exp in self.split_expressions_by_and(temp_list):
                expression_list.append(expression.Expression(exp))

        if token.ASTERISK in projection_list:
            projection_list = self.astrix_select(table_list)


        return (projection_list, table_list, expression_list)


    ###############################################################
    def split_expressions_by_and(self, _lst):
        sublists = [[]]
        for item in _lst:
            if item.literal.lower() == "and":
                sublists.append([])
            else:
                sublists[-1].append(item)
        return sublists


    def astrix_select(self, _table_list):
        db_schema = settings.DB_SCHEMA
        prj_list = set()
        for table in _table_list:
            table_cols = db_schema.get(table)
            for cl in table_cols.keys():
                prj_list.add(cl)

        return prj_list

    ###############################################################
    def expect_peek(self, type):
        if self.peek_token_is(type):
            self.next_token()
            return True
        else:
            self.peek_error(type)
            return False

    def expect_curr(self, type):
        if self.curr_token_is(type):
            self.next_token()
            return True
        else:
            self.curr_error(type)
            return False

    def curr_token_is(self, type):
        return self.curr_token.token_type == type
    
    def peek_token_is(self, type):
        return self.peek_token.token_type == type

    def peek_error(self, type):
        print(">>> PARSE ERORR: expected next token to be "+ str(type) +", got "+ str(self.peek_token.token_type) +" instead")

    def curr_error(self, type):
        print(">>> PARSE ERORR: expected current token to be "+ str(type) +", got "+ str(self.curr_token.token_type) +" instead")
