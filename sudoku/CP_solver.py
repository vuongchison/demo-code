class Variable:
    UNASSIGNED_FLAG = object()

    def __init__(self, domains: set):
        self.domains = domains
        self.value = self.UNASSIGNED_FLAG
    
    def is_assigned(self):
        return self.value != self.UNASSIGNED_FLAG
    
    def assign(self, value):
        assert value in self.domains
        self.value = value
    
    def unassign(self):
        self.value = self.UNASSIGNED_FLAG

    def remove_from_domain(self, value):
        self.domains.discard(value)
    
    def add_to_domain(self, value):
        self.domains.add(value)

    def __repr__(self):
        return self.domains.__repr__()

class Constraint:

    def __init__(self, variables: list):
        self.variables = variables

    def is_satisfied(self):
        pass
    def propagate(self, variable: Variable, value) -> tuple:
        pass

class NotEqualConstraint(Constraint):

    def __init__(self, x: Variable, y: Variable):
        super().__init__([x, y])
        self.x = x
        self.y = y

    def is_satisfied(self):
        if self.x.is_assigned() and self.y.is_assigned():
            return self.x.value != self.y.value
        if self.x.is_assigned():
            return len(self.y.domains - {self.x.value}) > 0
        if self.y.is_assigned():
            return len(self.x.domains - {self.y.value}) > 0
        return len(self.x.domains | self.y.domains) >= 2
    
    def propagate(self, variable: Variable, value) -> tuple:
        if variable == self.x and not self.y.is_assigned():
            self.y.remove_from_domain(value)
            return (self.y, value)
        if variable == self.y and not self.x.is_assigned():
            self.x.remove_from_domain(value)
            return (self.x, value)
        return None

from collections import defaultdict

class CPSolver:
    def __init__(self, variables: list[Variable], constraints: list[Constraint]):
        self.variables = variables
        self.constraints = constraints
        self.solution = dict()
        self.v_c_map = defaultdict(list)
        for c in self.constraints:
            for v in c.variables:
                self.v_c_map[v].append(c)


    def solve(self):
        self.backtrack()
        return self.solution

    def backtrack(self):
        var = self.select_unassigned_variable()
        if var is None:
            for v in self.variables:
                self.solution[v] = v.value
            return True
        
        for value in var.domains:
            var.assign(value)
            if self.is_satisfied(var):
                changes = self.propagate(var, value)
                if self.backtrack():
                    return True
                self.restore(changes)
            var.unassign()
        return False

    def is_satisfied(self, variable: Variable):
        return all((c.is_satisfied() for c in self.v_c_map[variable]))

    def select_unassigned_variable(self):
        for variable in self.variables:
            if not variable.is_assigned():
                return variable
        return None
    
    def propagate(self, variable, value) -> list[tuple]:
        changes = []
        for c in self.v_c_map[variable]:
            change = c.propagate(variable, value)
            if change is not None:
                changes.append(change)
        return changes

    def restore(self, changes: list[tuple]):
        for var, val in changes:
            var.add_to_domain(val)
