import time
import heapq 

directions = ["U", "D", "R", "L"]
input_files = ["test1.txt", "test2.txt", "test3.txt"]

class Node:
    def __init__(self, parent = None, state = None, action = None, path_cost = int(0), heuristic = None):
        self.parent = parent
        self.state = state
        self.action = action
        self.path_cost = path_cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.path_cost < other.path_cost)

class State:
    def __init__(self):
        self.snake = list()
        self.seeds = list()
    
    def __hash__(self):
        return hash((tuple(str(self.snake)), tuple(str(self.seeds))))

    def __eq__(self, other):
        return (self.snake == other.snake and self.seeds == other.seeds)


def heuristic(num, state, map_size):
    if num == 1:
        return find_heuristic_1(state)
    elif num == 2:
        return find_heuristic_2(state, map_size)

def find_heuristic_1(state):
    return len(state.seeds)

def find_heuristic_2(state, map_size):
    if len(state.seeds) == 0:
        return int(0)

    length = map_size[0]
    width = map_size[1]

    result = list()
    head = state.snake[-1]

    for i in state.seeds:
        x = abs(head[0] - i[0])
        y = abs(head[1] - i[1])
        distance = min(x, length-x) + min(y, width-y)
        result.append(distance)

    return max(result)

def A_star(start, map_size, heuristic_num):
    frontier = list()
    explored = dict()

    states = int(1)
    separates_states = int(1)

    heapq.heappush(frontier, (start.heuristic + start.path_cost, start))
    explored[start.state] = start.heuristic + start.path_cost

    while frontier:
        x = heapq.heappop(frontier)[1]

        if len(x.state.seeds) == 0:
            result = list()
            search = x
            while search.parent != None:
                result.append(search.action)
                search = search.parent

            return result, x.path_cost, states, separates_states

        head = x.state.snake[-1]

        for i in directions:
            if len(x.state.snake) >= 2:
                if x.action == "U" and i == "D" or x.action == "D" and i == "U":
                    continue
                elif x.action == "R" and i == "L" or x.action == "L" and i == "R":
                    continue

            _new_state = new_state(head, x.state, i, map_size)
            states += 1 
            heuristic_value = heuristic(heuristic_num, _new_state, map_size)

            if _new_state not in explored or heuristic_value + x.path_cost + 1 < explored[_new_state]: 
                heapq.heappush(frontier, (heuristic_value +  x.path_cost + 1,
                    Node(x, _new_state, i, x.path_cost + 1, heuristic_value)))
                explored[_new_state] = heuristic_value + x.path_cost + 1  
                separates_states += 1       

def check_collision(state, new_head):
    if len(state.snake) > 2 and new_head == state.snake[0]:
        return True
    return False if new_head in state.snake else True

def check_seed_existence(new_head, state):
    seed_1 = new_head + [1]
    seed_2 = new_head + [2]

    if seed_1 in state.seeds:
        state.snake.append(new_head)
        state.seeds.remove(seed_1)

    elif seed_2 in state.seeds:
        state.seeds.remove(seed_2)
        state.seeds.append(seed_1)
        state.snake.append(new_head)

    else:
        state.snake.pop(0)
        state.snake.append(new_head)

    return state

def new_state(head, state, action, map_size):
    new_state = State()
    new_state.snake = state.snake.copy()
    new_state.seeds = state.seeds.copy()
    
    if action == "R":
        new_head = check_border([head[0], head[1]+1], map_size)
    elif action == "L":
        new_head = check_border([head[0], head[1]-1], map_size)
    elif action == "U":
        new_head = check_border([head[0]-1, head[1]], map_size)
    elif action == "D":
        new_head = check_border([head[0]+1, head[1]], map_size)

    if check_collision(new_state, new_head):
        new_state = check_seed_existence(new_head, new_state)
    
    return new_state

def check_border(coordinates, map_size):
    length = map_size[0]
    width = map_size[1]

    if coordinates[0] == -1:
        coordinates[0] = length - 1
    if coordinates[0] == length:
        coordinates[0] = 0
    if coordinates[1] == -1:
        coordinates[1] = width - 1
    if coordinates[1] == width:
        coordinates[1] = 0
    return coordinates

def get_input(file_name):
    seeds_info = list()
    _file = open(file_name, "r")
    lines = _file.readlines()

    for i in range(len(lines)):
        if i == 0:
            map_size = [int(x) for x in lines[i].split(",")]
        elif i == 1:
            start = [int(x) for x in lines[i].split(",")]
        elif i == 2:
            seeds_num = int(lines[i])
        else:
            seeds_info.append([int(x) for x in lines[i].split(",")])
    _file.close()
    return start, map_size, seeds_info

def main():
    print("A star Algoritm:")
    for i in range(2):
        heuristic_num = i + 1

        for i in range(len(input_files)):
            start, map_size, seeds_info = get_input(input_files[i])

            new_state = State()
            new_state.snake.append(start)
            new_state.seeds = seeds_info
            new_node = Node(None, new_state, None, int(0), heuristic(heuristic_num, new_state, map_size))

            start_time = time.process_time() 
            result, path_cost, states, separates_states = A_star(new_node, map_size, heuristic_num)
            end_time = time.process_time() 

            print("***********************************")
            print("Test:", i+1)
            result.reverse()
            print("Path cost: ", path_cost)
            print("Path: ", result)
            print("Time: ", end_time - start_time, "s")
            print("States Number: ", states)
            print("Separate states Number: ", separates_states)
            print("###################################")

if __name__ == "__main__":
    main()