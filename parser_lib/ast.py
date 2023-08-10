####### Constants #######
ASSIGN_STM = "ASSIGNMENT"
IF_STM = "IF"
WHILE_STM = "WHILE"
OUT_STM = "OUTPUT"
SKIP_STM = "SKIP"

####### Base Node Class
class StmNode():
    def __init__(self, _type):
        self.node_type = _type

#######
class SkipNode(StmNode):
    def __init__(self):
        StmNode.__init__(self, SKIP_STM)

    def __str__(self):
        return str("Skip node")
    
    def __repr__(self):
        return str(self)

    def get_vars(self):
       return set()

#######
class AssignNode(StmNode):
    def __init__(self, _idnt, _exp):
        StmNode.__init__(self, ASSIGN_STM) 
        self.idnt = _idnt
        self.exp = _exp

    def __str__(self):
        return str("Assignment node :: Identifier: " + str(self.idnt) + ", Expression: " + str(self.exp))
    
    def __repr__(self):
        return str(self)

    def get_vars(self):
        vars = self.exp.get_vars()
        vars.add(self.idnt.literal)
        return vars

#######
class IfNode(StmNode):
    def __init__(self, _exp, _then_stm, _else_stm):
        StmNode.__init__(self, IF_STM) 
        self.exp = _exp
        self.then_stm = _then_stm
        self.else_stm = _else_stm

    def __str__(self):
        return str("If node :: Guard: " + str(self.exp) + ", Then: " + str(self.then_stm) + ", Else: " + str(self.else_stm))
    
    def __repr__(self):
        return str(self)

    def get_vars(self):
        vars = self.exp.get_vars()
        
        for stm in self.then_stm:
            vars = vars.union(stm.get_vars())

        for stm in self.else_stm:
            vars = vars.union(stm.get_vars())

        return vars

#######
class WhileNode(StmNode):
    def __init__(self, _exp, _body_stm):
        StmNode.__init__(self, WHILE_STM) 
        self.exp = _exp
        self.body_stm = _body_stm

    def __str__(self):
        return str("While node :: Guard: " + str(self.exp) + ", Body: " + str(self.body_stm))
    
    def __repr__(self):
        return str(self)

    def get_vars(self):
        vars = self.exp.get_vars()
        
        for stm in self.body_stm:
            vars = vars.union(stm.get_vars())

        return vars

#######
class OutNode(StmNode):
    def __init__(self, _exp, _user):
        StmNode.__init__(self, OUT_STM) 
        self.exp = _exp
        self.user = _user

    def __str__(self):
        return str("Output node :: Output: " + str(self.exp) + ", User: " + str(self.user))
    
    def __repr__(self):
        return str(self)

    def get_vars(self):
        vars = self.exp.get_vars()
        vars.add(self.user.literal)
        return vars