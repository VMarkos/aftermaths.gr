import entities
import search

def init_problem():
    DOMAIN = [4, 5, 6, 7, 8]
    VALUES = [4, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8]
    VALUES.reverse()
    variables = []
    for i in range(12):
        var = entities.Variable(DOMAIN)
        variables.append(var)
    constraints = []
    constraints.append(entities.Constraint(variables[0:3], lambda vars : vars[0].value + vars[1].value + vars[2].value, 17))
    constraints.append(entities.Constraint([variables[3], variables[4], variables[5]], lambda vars : vars[0].value + vars[1].value + vars[2].value, 17))
    constraints.append(entities.Constraint(variables[6:9], lambda vars : vars[0].value + vars[1].value + vars[2].value, 15))
    constraints.append(entities.Constraint(variables[9:12], lambda vars : vars[0].value + vars[1].value + vars[2].value, 20))
    constraints.append(entities.Constraint([variables[3], variables[6], variables[9]], lambda vars : vars[0].value + vars[0].value + vars[0].value, 17))
    constraints.append(entities.Constraint([variables[0], variables[7], variables[10]], lambda vars : vars[0].value + vars[1].value + vars[2].value, 17))
    constraints.append(entities.Constraint([variables[1], variables[4], variables[11]], lambda vars : vars[0].value + vars[1].value + vars[2].value, 15))
    constraints.append(entities.Constraint([variables[2], variables[5], variables[8]], lambda vars : vars[0].value + vars[1].value + vars[2].value, 20))
    constraints.append(entities.Constraint([variables[2], variables[4], variables[7], variables[9]], lambda vars : vars[0].value + vars[1].value + vars[2].value + vars[3].value, 23))
    init_state = entities.State(constraints, variables, VALUES)
    return init_state

def main():
    print("start")
    init_state = init_problem()
    # print(init_state)
    # print(init_state.exists_partition(23, 4, init_state.available_values))
    result = search.dfs(init_state, [], [init_state])
    print(result)

if __name__ == "__main__":
    main()
