# import random
import copy

import exceptions

class Variable:
    def __init__(self, domain):
        self.domain = domain
        self.value = 0

    def prune_domain(self, values):
        for x in values:
            if x in self.domain:
                self.domain.remove(x)

    def extend_domain(self, values):
        self.domain += values

    def is_assigned(self):
        return not self.value == 0

    def set_value(self, value):
        if not value in self.domain:
            raise exceptions.InvalidValueException()
        self.value = value
        
    def is_domain_empty(self):
        return len(self.domain) == 0

    def __str__(self):
        if self.value == 0:
            return "  "
        return str(self.value) + " "

class Constraint:
    def __init__(self, variables, constraint_fn, check_value):
        self.variables = variables
        self.constraint_fn = constraint_fn # Function with self.variables as argument and boolean output (true if it holds and false otherwise)
        self.check_value = check_value

    def current_value(self):
        return self.constraint_fn(self.variables)

    def is_violated(self):
        for var in self.variables:
            if not var.is_assigned():
                return False
        return not self.constraint_fn(self.variables) == self.check_value

    def unassigned_variables(self):
        n = 0
        for var in self.variables:
            if not var.is_assigned():
                n += 1
        return n

class State:
    def __init__(self, constraints, variables, available_values, n_rows = 4, n_cols = 4): # n_vars: int, domains: list of constraints.
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.variables = variables
        self.constraints = constraints
        self.available_values = available_values

    def __eq__(self, other):
        if not other.n_rows == self.n_rows:
            return False
        if not other.n_cols == self.n_cols:
            return False
        if not self.available_values == other.available_values:
            return False
        for i in range(len(self.variables)):
            if not self.variables[i].domain == other.variables[i].domain:
                return False
        not_equal = False
        for i in range(len(self.variables)):
            if not self.variables[i].value == other.variables[i].value:
                not_equal = True
                break
        if not_equal and not self.is_symmetric(other):
            return False
        return True

    def is_symmetric(self, other):
        sym_pairs = [(0, 3), (1, 6), (2, 9), (4, 7), (5, 10), (8, 11)]
        for (i, j) in sym_pairs:
            if not self.variables[i].value == other.variables[j].value:
                return False
            if not self.variables[j].value == other.variables[i].value:
                return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def assign_to(self, var_index, value):
        if not self.variables[var_index].value == 0:
            # print("asd")
            raise exceptions.AlreadyAssignedException()
        if not value in self.available_values:
            # print("asdas")
            raise exceptions.UnavailableValueException()
        try:
            self.remove_value(value)
        except Exception as e:
            print("103", e)
        self.variables[var_index].set_value(value)
        for constraint in self.constraints:
            remaining_value = constraint.check_value - constraint.current_value()
            # print(remaining_value)
            for var in self.variables:
                # print(self.available_values)
                try:
                    to_be_pruned = self.exists_partition(remaining_value, constraint.unassigned_variables(), self.available_values)
                except Exception as e:
                    print("110", e, e.args)
                # print(to_be_pruned)
                # for value in var.domain:
                    # if value > remaining_value or not value in self.available_values:
                    #     to_be_pruned.append(value)
                if to_be_pruned:
                    var.prune_domain(to_be_pruned)

    def exists_partition(self, n, m, values): # Returns the unused values (if any) for any partition
        # print(values)
        values = sorted(values)
        values.reverse()
        # print(values)
        partial_partitions = []
        for i in range(len(values) - 1):
            # print(partial_partitions)
            partial_partitions.insert(0, [[values[i]], values[i + 1:]]) # Stack, items of the form [partial partition, remaining values]
        # print("PP")
        # print(partial_partitions)
        complete_partitions = [] # List
        unused_values = [x for x in set(values)]
        while len(partial_partitions) > 0:
            # print(partial_partitions)
            pp = partial_partitions.pop()
            # print("pp:", len(pp[0]))
            if len(pp[0]) == m and sum(pp[0]) == n:
                # print("found")
                for x in pp[0]:
                    if x in unused_values:
                        unused_values.remove(x)
                    if len(unused_values) == 0:
                        # print("none")
                        return []
                if not pp[0] in complete_partitions:
                    complete_partitions.append(pp[0])
            elif len(pp[0]) == m or sum(pp[0]) > n:
                # print("failed", pp[0])
                continue
            else:
                # print("else")
                if pp[1] == None or len(pp[1]) == 0:
                    continue
                for value in pp[1]:
                    # print("value:", value)
                    try:
                        copycat = [x for x in pp[1]]
                        copycat.remove(value)
                        # print("after removal:", pp[0], value, copycat)
                        partial_partitions.append([
                            pp[0] + [value],
                            copycat
                        ])
                    except Exception as e:
                        print("161", e)
        #     print("new pp:", len(partial_partitions))
        # print(n, m, values, complete_partitions)
        # print("unused:", unused_values)
        return unused_values

    def get_children(self):
        children = []
        for i in range(len(self.variables)):
            if not self.variables[i].is_assigned():
                for value in set(self.available_values):
                    child = self.copy()
                    # print(value)
                    try:
                        child.assign_to(i, value)
                        # print("child:", child)
                        # print("is_valid:", child.is_valid())
                        if child.is_valid() and not child in children:
                            children.append(child)
                    except Exception as e:
                        # print("180", e)
                        continue
        return children

    def prune_domains(self):
        """
        In domain pruning, you iterate over all variables and:
            For each value of each var:
                check all constraints and if some is violated, remove that value from its domain.
        """
        for variable in self.variables:
            for value in variable.domain:
                to_be_pruned = []
                previous_value = variable.value
                variable.set_value(value)
                for constraint in self.constraints:
                    if constraint.is_violated():
                        to_be_pruned.append(value)
                variable.set_value(previous_value)
                variable.prune_domain(to_be_pruned)

    def forward_checking(self, depth = 3):
        i = 0
        closed = []
        front = [None, self]
        if len(front) > 0:
            state = front.pop()
        else:
            return False
        while i < depth and len(front) > 0:
            if not state:
                state = front.pop()
                front = [None] + front
                i += 1
            elif state.is_complete():
                return True
            if state in closed:
                state = front.pop()
            else:
                front = state.get_children() + front
                closed.append(state)
                state = front.pop()
        if i == depth and len(front) > 0:
            return True
        return False

    def remove_value(self, value):
        if value in self.available_values:
            self.available_values.remove(value)

    def is_valid(self):
        for var in self.variables:
            if var.is_domain_empty():
                return False
        for constraint in self.constraints:
            if constraint.is_violated():
                return False
        return True

    def is_complete(self):
        if not self.is_valid():
            return False
        for var in self.variables:
            if not var.is_assigned():
                return False
        return True

    def __str__(self):
        values = [6, 6, 8, 3]
        state_str = ""
        index = 0
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if i == j:
                    state_str += str(values[i]) + " "
                else:
                    state_str += self.variables[index].__str__()
                    index += 1
            state_str += "\n"
        return state_str
