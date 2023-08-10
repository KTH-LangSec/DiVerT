import label_lib.formula as formula_lib

class SymbolicTuple:
    def __init__(self, _projection_list, _table_list, _expression_list):
        self.columns = _projection_list.copy()
        self.table_names = _table_list.copy()
        self.phi = formula_lib.Conjunction(_expression_list)
    
    def __str__(self):
        result = "< "

        if self.table_names:
            result += str(self.table_names) + ", "
        else:
            result += "{}, "

        result += str(self.phi) + ", "

        if self.columns:
            result += str(self.columns)
        else:
            result += "{}"
            
        result += " >"
        return result

    def __repr__(self):
        return str(self)