import z3
import query_lib.token as Qtoken
import query_lib as query_lib
import settings 


class Z3Solver():
    def __init__(self):
        self.slv = z3.Solver()

        self.tables_columns = {} # A dict of all of the columns in the database
        for cols in settings.DB_SCHEMA.values():
            self.tables_columns.update(cols)


    def check_not_implication_sat(self, _left_phi, _right_phi):



        con_left = z3.And(self.process_formula(_left_phi))
        con_right = z3.And(self.process_formula(_right_phi))

        imp = z3.Implies(con_left, con_right)
        self.slv.add(z3.Not(imp))

        # if settings.DEBUG:
        #     print("Solver:")
        #     print("\tFormula: ",end="")
        #     print(self.slv)
        #     if (self.slv.check().r == 1):
        #         print("\tResult: Sat")
        #         print("\tModel: ",end="")
        #         print(self.slv.model()) 
        #     else:
        #         print("Result: unSat")

        if (self.slv.check().r == 1):
            return True  # sat
        else:
            return False # unsat

    def process_formula(self, _phi):
        if not _phi.expressions:
            return True

        lst = []
        for exp in _phi.expressions:
            lst.append(self.process_exp(exp.expression))

        return lst

    def process_exp(self, _exp):
        if isinstance(_exp, query_lib.expression.InfixExpressionNode):
            match _exp.token.token_type:
                case Qtoken.EQ:
                    return (self.process_exp(_exp.left_exp) == self.process_exp(_exp.right_exp))
                case Qtoken.NOT_EQ:
                    return (self.process_exp(_exp.left_exp) != self.process_exp(_exp.right_exp))
                case Qtoken.LT:
                    return (self.process_exp(_exp.left_exp) < self.process_exp(_exp.right_exp))
                case Qtoken.GT:
                    return (self.process_exp(_exp.left_exp) > self.process_exp(_exp.right_exp))
                case Qtoken.PLUS:
                    return (self.process_exp(_exp.left_exp) + self.process_exp(_exp.right_exp))
                case Qtoken.MINUS:
                    return (self.process_exp(_exp.left_exp) - self.process_exp(_exp.right_exp))
                case Qtoken.ASTERISK:
                    return (self.process_exp(_exp.left_exp) * self.process_exp(_exp.right_exp))
                case Qtoken.SLASH:
                    return (self.process_exp(_exp.left_exp) / self.process_exp(_exp.right_exp))
        elif isinstance(_exp, query_lib.expression.PrefixExpressionNode):
            match _exp.token.token_type:
                case Qtoken.MINUS:
                    return (-(self.process_exp(_exp.right_exp)))
                case Qtoken.BANG:
                    return (z3.Not(self.process_exp(_exp.right_exp)))
        elif isinstance(_exp, query_lib.expression.IdentifierNode):
            if self.tables_columns[_exp.value] == Qtoken.INT:
                    return z3.Int(_exp.value)
            elif self.tables_columns[_exp.value] == Qtoken.BOOL:
                    return z3.Bool(_exp.value)
            elif self.tables_columns[_exp.value] == Qtoken.STR:
                    return z3.String(_exp.value)
        elif isinstance(_exp, query_lib.expression.IntegerNode):
            return int(_exp.value)
        elif isinstance(_exp, query_lib.expression.BooleanNode):
            return _exp.value
        elif isinstance(_exp, query_lib.expression.StringNode):
            return str(_exp.value)




        return False

