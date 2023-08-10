
class Formula():
    def __init__(self):
        pass

class Conjunction(Formula):
    def __init__(self, _expression_list):
        self.expressions = []
        for exp in _expression_list:
            self.expressions.append(exp)

    def get_vars(self):
        vars = set()
        for exp in self.expressions:
            vars = vars.union(exp.get_vars())

        return vars


    def __str__(self):
        if not self.expressions:
            return "true"
        else:
            res = ""
            for con in self.expressions:
                res += str(con) + " ∧ "
            res = res[:-3]
            res += ""

            return res