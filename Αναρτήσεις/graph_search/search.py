import json

def dfs(state, closed, front):
    queue = ""
    while len(front) > 0:
        queue += state.__str__() + "\n-------------------\n"
        if state.is_complete():
            print("complete")
            print(state)
            return state
        if state in closed:
            state = front.pop()
        else:
            children = state.get_children()
            print(len(front), len(closed))
            front += children
            closed.append(state)
            state = front.pop()
            while not state.forward_checking() and len(front) > 0:
                state = front.pop()
    with open("queue_fc.txt", "w") as file:
        file.write(queue)