import parser_lib.token as Ptoken
import label_lib

def compute_vars(_stms):
    vars = set()

    ## adding pc
    vars.add("pc")

    for stm in reversed(_stms):
        vars = vars.union(stm.get_vars())
    
    return vars


def tensor_two_sets_of_sets(_set1, _set2):
    result = set()
    for s1 in _set1:
        for s2 in _set2:
            result.add(frozenset(set(s1).union(s2)))

    return result


def tensor(_lst):
    if len(_lst) == 1:
        return _lst[0]
    if len(_lst) == 2:
        return tensor_two_sets_of_sets(_lst[0], _lst[1])
    elif len(_lst) > 2:
        tmp = []
        for i in _lst[2:]:
            tmp.append(i)
        tmp.append(tensor_two_sets_of_sets(_lst[0], _lst[1]))
        return tensor(tmp)
    else:
        print("Tensor Error!")
        return None


def gamma_vars_to_lst(_vars, _gamma):
    result = []
    for var in _vars:
        if type(var) is str:
            result.append(_gamma[var])
        elif isinstance(var, Ptoken.Token):
            tmp = set()
            tmp.add(frozenset([var]))
            result.append(tmp)
    return result


def generate_set_of_sets(*args):
    dep_set = set()
    for itm in args:
        dep_set = dep_set.union(itm)

    result_set = set()
    result_set.add(frozenset(dep_set))

    return result_set


def str_forzensets(_fsets):
    res = "{ "
    for fset in _fsets:
        res += str(set(fset)) + ", "
    res = res[:-2]
    res += " }"
    return res
    



## Extracts the symbolic tuples from the dependency set
## This function ignores the variables, and only maps the queries to symbolic tuples.
def sts(_dep_sets):
    set_of_labels = set()
    for subset in _dep_sets:
        only_query_subset = set()
        for s in subset:
            if isinstance(s, Ptoken.Token):
                only_query_subset.add(s.literal)
        label = label_lib.get_label(only_query_subset)
        set_of_labels.add(label)

    return set_of_labels


## STS function, but for policies
def sts_policy(_policy):
    if (not _policy) or ( _policy.token_type != Ptoken.POLICY):
        return set()

    set_of_labels = set()
    for con in _policy.literal:
        query_subset = set()
        for q in con:
            query_subset.add(q)
        label = label_lib.get_label(query_subset)
        set_of_labels.add(label)

    return set_of_labels



if __name__ == "__main__":
    # gamma = {}
    # gamma["x"] = [["x"], ["w"], ["z"]]
    # gamma["y"] = [["y"], ["m"]]
    # gamma["a"] = [["b"], ["c"]]
    # gamma["f"] = [["f"], ["u"]] ## should be ignored

    # tmp = gamma_vars_to_lst(["x"],gamma)
    # print(tmp)


    set1 = set()
    set1.add(frozenset(["x"]))
    set1.add(frozenset(["w"]))
    set1.add(frozenset(["z"]))
    
    set2 = set()
    set2.add(frozenset(["y"]))
    set2.add(frozenset(["m"]))

    set3 = set()
    set3.add(frozenset(["b"]))
    set3.add(frozenset(["c"]))

    print(tensor([set1, set2, set3]))

