import timeit
from queue import PriorityQueue
import os

input_name = ''


# -------------------------Node--------------------------
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
        if x % n == n - 1:
            moves.remove('Right')
        if x - n < 0:
            moves.remove('Up')
        if x + n > n * n - 1:
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


# -------------------Search Algorithms-------------------
def dijkstra(initial_state, goal, n):
    frontier = PriorityQueue()
    explored = set()
    counter = 0
    root = State(initial_state, goal, None, None, 0)
    frontier.put((root.depth, counter, root))
    while not frontier.empty():
        current_node = frontier.get()
        current_node = current_node[2]
        explored.add(current_node.map)
        if current_node.test():
            return current_node.solution()

        children = current_node.expand(n)
        for child in children:
            if child.map not in explored:
                counter += 1
                frontier.put((child.depth, counter, child))
                explored.add(child.map)
    return []


def bidirectional_ucs(initial_state, goal, n):
    frontier1, frontier2 = PriorityQueue(), PriorityQueue()
    explored1, explored2 = set(), set()
    counter1, counter2 = 0, 0
    root1 = State(initial_state, goal, None, None, 0)
    root2 = State(goal, initial_state, None, None, 0)
    frontier1.put((root1.depth, counter1, root1))
    frontier2.put((root2.depth, counter2, root2))

    path1, path2 = {root1.map: []}, {root2.map: []}
    weights1, weights2 = {root1.map: 0}, {root2.map: 0}
    best_path = []
    mu = float('inf')

    while not frontier1.empty() and not frontier2.empty():
        current_node1 = frontier1.get()
        cost1 = current_node1[0]
        current_node2 = frontier2.get()
        cost2 = current_node2[0]
        node1 = current_node1[2]
        node2 = current_node2[2]
        weights1[node1.map], weights2[node2.map] = cost1, cost2
        explored1.add(node1.map)
        explored2.add(node2.map)

        if node1.map in path2.keys() and weights1[node1.map] + weights2[node1.map] < mu:
            best_path = path1[node1.map] + [node1.state] + path2[node1.map]
            mu = weights1[node1.map] + weights2[node1.map]

        children1 = node1.expand(n)
        for child in children1:
            if child.map not in explored1:
                if weights1.get(child.map, float('inf')) > cost1:
                    counter1 += 1
                    weights1[child.map] = cost1
                    path1[child.map] = path1[node1.map] + [node1.state]
                    frontier1.put((child.depth, counter1, child))
                    explored1.add(child.map)

        if node2.map in path1.keys() and weights1[node2.map] + weights2[node2.map] < mu:
            best_path = path1[node2.map] + [node2.state] + path2[node2.map]
            mu = weights1[node2.map] + weights2[node2.map]

        children2 = node2.expand(n)
        for child in children2:
            if child.map not in explored2:
                if weights2.get(str(child.state), float('inf')) > cost2:
                    counter2 += 1
                    weights2[child.map] = cost2
                    path2[child.map] = [node2.state] + path2[node2.map]
                    frontier2.put((child.depth, counter2, child))
                    explored2.add(child.map)
        if not frontier1.empty() and not frontier2.empty():
            top1, top2 = frontier1.queue[0][0], frontier2.queue[0][0]
            if top1 + top2 >= mu:
                best_path.pop(0)
                return best_path
        else:
            return []


# ------------------------Driver-------------------------
def write_in_file(file, text, time, states, n):
    file.write(f"{text}: \n")
    file.write("time " + format(time, '.8f') + "\n")
    if not len(states) == 0:
        states.pop()
    file.write("Act " + str(len(states)) + "\n")
    for state in states:
        file.write("\n")
        for _ in range(n):
            output = state[0: n]
            file.write(str(output).replace('[', ' ').replace(']', '\n').replace(',', '').replace("'", ''))
            state = state[n:]


def export(time_dijkstra, states_dijkstra, time_states_bidirectional_ucs, states_states_bidirectional_ucs, n):
    global input_name
    file = open(f'Log_{input_name.replace(".txt","")}_Shahabi.txt', 'w')
    file.write(f"{input_name} \n")
    file.write("\n")
    write_in_file(file, "Dijkstra", time_dijkstra, states_dijkstra, n)
    file.write("\n")
    write_in_file(file, "Bidirectional", time_states_bidirectional_ucs, states_states_bidirectional_ucs, n)
    file.close()


def read_input(file_location):
    global input_name
    root, goal, half, n = [], [], True, 0
    with open(file_location) as file:
        input_name = os.path.basename(file.name).split('/')[-1]
        for line in file:
            if line.strip():
                l = line.strip().split(" ")
                if '\n' in l:
                    l.remove('\n')
                if half:
                    n += 1
                    for item in l:
                        root.append(item)
                else:
                    for item in l:
                        goal.append(item)
            else:
                half = False
    return root, goal, n


def main():
    file_location = input("Enter file location (tests/t1.txt): ")
    root, goal, n = read_input(file_location)

    start_dijkstra = timeit.default_timer()
    states_dijkstra = dijkstra(root, goal, n)
    stop_dijkstra = timeit.default_timer()

    start_bidirectional_ucs = timeit.default_timer()
    states_bidirectional_ucs = bidirectional_ucs(root, goal, n)
    stop_bidirectional_ucs = timeit.default_timer()

    export(stop_dijkstra - start_dijkstra, states_dijkstra,
           stop_bidirectional_ucs - start_bidirectional_ucs, states_bidirectional_ucs, n)


if __name__ == '__main__':
    main()
