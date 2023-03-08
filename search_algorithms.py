from state import State
from queue import PriorityQueue


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
