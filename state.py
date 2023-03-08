class State:
    def __init__(self, state, goal, parent, direction, depth):
        self.state = state
        self.parent = parent
        self.direction = direction
        self.depth = depth
        self.goal = goal
        if self.state:
            self.map = ''.join(str(e) for e in self.state)

    def test(self):
        if self.state == self.goal:
            return True
        return False

    @staticmethod
    def available_moves(x, n):
        moves = ['Left', 'Right', 'Up', 'Down']
        if x % n == 0:
            moves.remove('Left')
        if x % n == n-1:
            moves.remove('Right')
        if x - n < 0:
            moves.remove('Up')
        if x + n > n*n - 1:
            moves.remove('Down')

        return moves

    def expand(self, n):
        try:
            x = self.state.index('*')
        except ValueError:
            x = self.state.index('**')
        moves = self.available_moves(x, n)
        
        children = []
        for direction in moves:
            temp = self.state.copy()
            if direction == 'Left':
                temp[x], temp[x - 1] = temp[x - 1], temp[x]
            elif direction == 'Right':
                temp[x], temp[x + 1] = temp[x + 1], temp[x]
            elif direction == 'Up':
                temp[x], temp[x - n] = temp[x - n], temp[x]
            elif direction == 'Down':
                temp[x], temp[x + n] = temp[x + n], temp[x]

            children.append(State(temp, self.goal, self, direction, self.depth + 1))
        return children

    def solution(self):
        solution = [self.state]
        path = self
        while path.parent is not None:
            path = path.parent
            solution.append(path.state)
        solution = solution[:-1]
        solution.reverse()
        return solution
         