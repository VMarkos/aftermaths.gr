class Board:
    def __init__(self, path, rows=3, cols=3):
        self.path = path
        self.rows = rows
        self.cols = cols
        self.NEXT = {
            (0, 0): [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
            (0, 1): [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
            (0, 2): [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
            (1, 0): [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)],
            (1, 1): [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
            (1, 2): [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)],
            (2, 0): [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
            (2, 1): [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
            (2, 2): [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
        }

    def is_complete(self):
        return len(self.path) == self.rows * self.cols

    def get_next(self):
        return [self.path + [node] for node in self.NEXT[self.path[-1]] if node not in self.path]
    
    def is_complete(self):
        return len(self.path) == self.rows * self.cols

    def __str__(self):
        board_str = ''
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) in self.path:
                    board_str += str(self.path.index((i, j))) + ' '
                else:
                    board_str += '. '
            board_str = board_str[:-1] + '\n'
        return board_str[:-1]

def count_patterns():
    rows = 3
    cols = 3
    front = [Board([(i, j)]) for i in range(rows) for j in range(cols)] # Stack with all currently active board states.
    count = 0
    while len(front) > 0:
        current_board = front.pop()
        if current_board.is_complete():
            count += 1
        next_paths = current_board.get_next()
        for path in next_paths:
            next_board = Board(path)
            front.append(next_board)
    return count

if __name__ == '__main__':
    n = count_patterns()
    print(n)