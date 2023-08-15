import helper
import parser_lib.ast as Past

#############################################################
class Gamma():
    def __init__(self, _input_stms, _vars):
        self.stms = _input_stms
        self.vars = _vars
        self.pc = "pc"

        self.generate_id()

        self.generate_gamma()

    ####### Generate the final Gamma environment #######
    def generate_gamma(self):
        self.env = self.id.copy()
        for stm in reversed(self.stms):
            self.env = self.seq_composition(self.generate_stm_gamma(stm), self.env)

    ####### Generate the identity Gamma environment #######
    def generate_id(self):
        self.id = {}
        for var in self.vars:
            result_set = set()
            result_set.add(frozenset([var]))
            self.id[var] = result_set

    ####### Generate Gamma environment for each statement #######
    def generate_stm_gamma(self, _stm):
        match _stm.node_type:
            case Past.SKIP_STM:
                return self.id
            case Past.ASSIGN_STM:
                return self.assignment_gamma(_stm)
            case Past.OUT_STM:
                return self.output_gamma(_stm)
            case Past.IF_STM:
                return self.if_gamma(_stm)
            case Past.WHILE_STM:
                return self.while_gamma(_stm)
            case _:
                return None

    ####### Generate Gamma environment for assignment statement #######
    def assignment_gamma(self, _stm):
        idnt = _stm.idnt
        gamma = self.id.copy()
        gamma[idnt.literal] = helper.generate_set_of_sets(_stm.exp.get_queries(), _stm.exp.get_vars(), set([self.pc]))
        return gamma

    ####### Generate Gamma environment for output statement #######
    def output_gamma(self, _stm):
        usr = _stm.user
        gamma = self.id.copy()
        gamma[usr.literal] = helper.generate_set_of_sets(_stm.exp.get_queries(), _stm.exp.get_vars(), set([self.pc]), set([usr.literal]))
        return gamma
    
    ####### Generate Gamma environment for if statement #######
    def if_gamma(self, _stm):
        id_env = self.id.copy()
        id_env[self.pc] = helper.generate_set_of_sets(_stm.exp.get_queries(), _stm.exp.get_vars(), set([self.pc]))

        gamma_1 = Gamma(_stm.then_stm, self.vars).env
        gamma_2 = Gamma(_stm.else_stm, self.vars).env

        gamma_prime_1 = self.seq_composition(id_env, gamma_1)
        gamma_prime_2 = self.seq_composition(id_env, gamma_2)

        result_env = self.disjunctive_union(gamma_prime_1, gamma_prime_2)
        result_env[self.pc] = helper.generate_set_of_sets(set([self.pc]))

        return result_env

    ####### Generate Gamma environment for while statement #######
    def while_gamma(self, _stm):
        id_env = self.id.copy()
        id_env[self.pc] = helper.generate_set_of_sets(_stm.exp.get_vars(), set([self.pc]))

        gamma_c = Gamma(_stm.body_stm, self.vars).env

        gamma_seq = self.seq_composition(id_env, gamma_c)

        gamma_f = self.fix_point(gamma_seq)

        gamma_f[self.pc] = helper.generate_set_of_sets(set([self.pc]))

        return gamma_f

    #######################################################################################
    #######################################################################################

    ####### Squential composition of two environments #######
    def seq_composition(self, _gamma_1, _gamma_2):
        gamma_res = _gamma_2.copy()
        for x in self.vars:
            res = set()
            for s2 in gamma_res[x]:
                lst = helper.gamma_vars_to_lst(s2, _gamma_1)
                tensor = set(helper.tensor(lst))
                res = res.union(tensor)
            
            gamma_res[x] = res

        return gamma_res

    ####### Disjunctive union of two environments #######
    def disjunctive_union(self, gamma_1, gamma_2):
        gamma = {}
        for x in self.vars:
            result_set = set()
            for _set1 in gamma_1[x]:
                result_set.add(_set1)
            for _set2 in gamma_2[x]:
                result_set.add(_set2)
            
            gamma[x] = result_set

        return gamma

    ####### Fix point of an environment #######
    def fix_point(self, _gamma):
        gamma = _gamma.copy()
        gamma_next = self.seq_composition(gamma, gamma)
        while not self.equals(gamma,gamma_next):
            gamma = gamma_next.copy()
            gamma_next = self.seq_composition(gamma_next, gamma_next)

        return gamma_next

    ####### Check the equality of two environments #######
    def equals(self, gamma_1, gamma_2):
        for x in self.vars:
            if (gamma_1[x] != gamma_2[x]):
                return False

        return True

    #######   #######
    # def __str__(self):
    #     res = "[ "
    #     for k,v in self.env.items():
    #         res += str(k) + " ↦ " + str(v) + ", "
    #     res = res[:-2]
    #     res += " ]"
    #     return res

    #######   #######
    def __str__(self):
        res = "\n"
        for k,v in self.env.items():
            res += "\t\t" + str(k) + " ↦ " + helper.str_forzensets(v) + "\n"
        res = res[:-1]
        return res

    #######   #######
    def __repr__(self):
        return str(self)
