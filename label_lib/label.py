import label_lib.label_helper as lb_helper

class Label():
    def __init__(self):
        self.st_set = set()

    def add_st(self, _st):
        self.st_set.add(_st)

    def is_less_than(self, other_label):
        return lb_helper.label_leq_label(self, other_label)


    def __str__(self):
        if not self.st_set:
            return "{}"
        else:
            result = "{ "
            for st in self.st_set:
                result += str(st) + ", "
            result = result[:-2]
            result += " }"
            return result

    def __repr__(self):
        return str(self)