import timeit
from search_algorithms import dijkstra, bidirectional_ucs
import os

input_name = ''


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
