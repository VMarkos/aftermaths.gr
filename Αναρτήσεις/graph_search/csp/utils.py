import entities

def find_partitions(n, m, values):
    """
    Partitions n into a sum of m positive integers from values:
        * n: the number to be partitioned;
        * m: the number of partitioning integers;
        * values: the list of possible values --- including repetitions, i.e., [1, 1, 2] means that 1 miht be used twice.
    """
    values = sorted(values)
    values.reverse()
    partial_partitions = []
    for i in range(len(values) - 1):
        partial_partitions.insert(0, [entities.MultiSet([values[i]]), values[i + 1:]]) # Stack, items of the form [partial partition, remaining values]
    complete_partitions = [] # List
    while len(partial_partitions) > 0:
        pp = partial_partitions.pop()
        if len(pp[0]) == m and sum(pp[0]) == n and not pp[0] in complete_partitions:
            complete_partitions.append(pp[0])
        elif len(pp[0]) == m or sum(pp[0]) > n or len(pp[1]) == 0: # or pp[1] == None?
            continue
        for i in range(len(pp[1]) - 1, -1, -1):
            value = pp[1][i]
            copycat = [x for x in pp[1]]
            copycat.remove(value)
            partial_partitions.append([
                pp[0] + entities.MultiSet([value]),
                copycat
            ])
    return complete_partitions