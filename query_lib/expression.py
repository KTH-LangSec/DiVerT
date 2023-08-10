import query_lib.token as token

####### PRECEDENCE CONSTANTS #######
LOWEST = 1
EQUALS = 2 # ==
LESSGREATER = 3 # > <
SUM = 4 # +
PRODUCT = 5 # *
PREFIX = 6 # -x

#######################################################
################## Expression Parser ##################
#######################################################
class exp_parser():
    def __init__(self, _exp_input_list):
        self.exp_list = _exp_input_list
        self.counter = 0

        self.curr_token = token.Token(token.ILLEGAL, "")
        self.peek_token = token.Token(token.ILLEGAL, "")

        # Read two tokens, so curr_token and peek_token are both set
        self.next_token()
        self.next_token()

        # expression parser function maps
        self.prefix_parse_fns = {}
        self.prefix_parse_fns[token.IDENT] = self.parse_identifier
        self.prefix_parse_fns[token.INT] = self.parse_integer
        self.prefix_parse_fns[token.BANG] = self.parse_prefix_expression
        self.prefix_parse_fns[token.MINUS] = self.parse_prefix_expression
        self.prefix_parse_fns[token.TRUE] = self.parse_boolean
        self.prefix_parse_fns[token.FALSE] = self.parse_boolean
        self.prefix_parse_fns[token.STR] = self.parse_string
        self.prefix_parse_fns[token.LPAREN] = self.parse_grouped_expression

        self.infix_parse_fns = {}
        self.infix_parse_fns[token.EQ] = self.parse_infix_expression
        self.infix_parse_fns[token.NOT_EQ] = self.parse_infix_expression
        self.infix_parse_fns[token.LT] = self.parse_infix_expression
        self.infix_parse_fns[token.GT] = self.parse_infix_expression
        self.infix_parse_fns[token.PLUS] = self.parse_infix_expression
        self.infix_parse_fns[token.MINUS] = self.parse_infix_expression
        self.infix_parse_fns[token.SLASH] = self.parse_infix_expression
        self.infix_parse_fns[token.ASTERISK] = self.parse_infix_expression

        # precedences table
        self.precedences = {}
        self.precedences[token.EQ] = EQUALS
        self.precedences[token.NOT_EQ] = EQUALS
        self.precedences[token.LT] = LESSGREATER
        self.precedences[token.GT] = LESSGREATER
        self.precedences[token.PLUS] = SUM
        self.precedences[token.MINUS] = SUM
        self.precedences[token.SLASH] = PRODUCT
        self.precedences[token.ASTERISK] = PRODUCT


    def next_token(self):
        self.curr_token = self.peek_token

        if (self.counter < len(self.exp_list)):
            self.peek_token = self.exp_list[self.counter]
        else:
            self.peek_token = token.Token(token.EOF, "")

        self.counter += 1


    def parse_expression(self, _precedence):
        prefix_fn = self.prefix_parse_fns.get(self.curr_token.token_type)

        if (prefix_fn == None):
            print(">>>> No prefix parse function for "+str(self.curr_token.token_type)+" found")
            return None

        left_exp = prefix_fn()

        while (self.peek_token.token_type != token.EOF and _precedence < self.peek_precedence()):
            infix_fn = self.infix_parse_fns.get(self.peek_token.token_type)
            if (infix_fn == None):
                return left_exp

            self.next_token()

            left_exp = infix_fn(left_exp)

        return left_exp
        

    def parse_identifier(self):
        return IdentifierNode(self.curr_token, self.curr_token.literal)


    def parse_integer(self):
        return IntegerNode(self.curr_token, self.curr_token.literal)

    def parse_boolean(self):
        return BooleanNode(self.curr_token, self.curr_token.literal)

    def parse_string(self):
        return StringNode(self.curr_token, self.curr_token.literal)

    def parse_grouped_expression(self):
        self.next_token()

        exp = self.parse_expression(LOWEST)

        if (not self.expect_peek(token.RPAREN)):
            return None

        return exp


    def parse_prefix_expression(self):
        exp_node = PrefixExpressionNode(self.curr_token, self.curr_token.literal, None)

        self.next_token()

        exp_node.right_exp = self.parse_expression(PREFIX)

        return exp_node


    def parse_infix_expression(self, _left_exp):
        exp_node = InfixExpressionNode(self.curr_token, _left_exp, self.curr_token.literal, None)

        prec = self.curr_precedence()
        self.next_token()
        exp_node.right_exp = self.parse_expression(prec)

        return exp_node


    def peek_precedence(self):
        prec = self.precedences.get(self.peek_token.token_type)
        if prec != None:
            return prec

        return LOWEST


    def curr_precedence(self):
        prec = self.precedences.get(self.curr_token.token_type)
        if prec != None:
            return prec

        return LOWEST

    def expect_peek(self, _type):
        if self.peek_token.token_type == _type:
            self.next_token()
            return True
        else:
            print(">>> EXPRESSION PARSE ERORR: expected next token to be "+ str(_type) +", got "+ str(self.peek_token.token_type) +" instead")
            return False


##########################################################
################## EXPRESSION AST NODES ##################
##########################################################
class IdentifierNode():
    def __init__(self, _tok, _val):
        self.token = _tok
        self.value = _val

    def __str__(self):
        return str(self.value)

class PrefixExpressionNode():
    def __init__(self, _tok, _opr, _rexp):
        self.token = _tok
        self.operator = _opr
        self.right_exp = _rexp

    def __str__(self):
        return "("+str(self.operator)+str(self.right_exp)+")"

class IntegerNode():
    def __init__(self, _tok, _val):
        self.token = _tok
        self.value = 0
        try:
            self.value = int(_val)
        except:
            print(">>>> Value "+ str(_val) +" cannot be converted to integer")

    def __str__(self):
        return str(self.value)

class BooleanNode():
    def __init__(self, _tok, _val):
        self.token = _tok
        if _val.lower() == "true":
            self.value = True
        else:
            self.value = False

    def __str__(self):
        return str(self.value)

class StringNode():
    def __init__(self, _tok, _val):
        self.token = _tok
        self.value = _val

    def __str__(self):
        return str("'"+self.value+"'")

class InfixExpressionNode():
    def __init__(self, _tok, _lexp, _opr, _rexp):
        self.token = _tok
        self.left_exp = _lexp
        self.operator = _opr
        self.right_exp = _rexp

    def __str__(self):
        return "("+str(self.left_exp)+str(self.operator)+str(self.right_exp)+")"


######################################################
################## Expression Class ##################
######################################################
class Expression():
    def __init__(self, _exp_input_lst):
        self.exp_list = _exp_input_lst
        self.expression = exp_parser(_exp_input_lst).parse_expression(LOWEST)

    #######
    def get_vars(self):
        vars = set()
        for tok in self.exp_list:
            if (tok.token_type == token.IDENT):
                vars.add(tok.literal)
        
        return vars

    #######
    def __str__(self):
        return str(self.expression)

    #######
    def __repr__(self):
        return str(self)