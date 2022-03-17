from copy import copy
from node import Move, Node


goal_node = Node(None, -1, ['1', '2', '3', '8', 'B', '4', '7', '6', '5'])
# goal_node = Node(None, -1, ['1', '2', '3', '4', '5', '6', '7', '8', 'B'])
test_node = Node(None, 1, ['1', '2', '3', 'B', '8', '4', '7', '6', '5'])

open = list()
closed = list()

path_length = int(0)

def display_board(state: list):
    print( "-------------")
    print( "| %s | %s | %s |" % (state[0], state[1], state[2]))
    print( "-------------")
    print( "| %s | %s | %s |" % (state[3], state[4], state[5]))
    print( "-------------")
    print( "| %s | %s | %s |" % (state[6], state[7], state[8]))
    print( "-------------")

def possible_moves(current_index_blank):
    possible_moves_list = set()

# Vertical Moves
    if current_index_blank in range(0, 3):
        possible_moves_list.add(Move.DOWN)
    elif current_index_blank in range(3, 6):
        possible_moves_list.add(Move.UP)
        possible_moves_list.add(Move.DOWN)
    else:
        possible_moves_list.add(Move.UP)
    
# Horizontal Moves
    if current_index_blank in [0, 3, 6]:
        possible_moves_list.add(Move.RIGHT)
    elif current_index_blank in [1, 4, 7]:
        possible_moves_list.add(Move.RIGHT)
        possible_moves_list.add(Move.LEFT)
    else:
        possible_moves_list.add(Move.LEFT)
    
    return possible_moves_list


def generate_children(node):
    new_children = list()
    current_index_blank = node.state.index('B')
    new_depth = node.depth + 1
    moves = possible_moves(current_index_blank)
    if(Move.DOWN in moves):
        swap_index = current_index_blank + 3
        new_state: list = copy(node.state)
        new_state[current_index_blank], new_state[swap_index] = new_state[swap_index], new_state[current_index_blank]
        new_node = Node(node, new_depth, new_state)
        new_children.append(new_node)
    if(Move.UP in moves):
        swap_index = current_index_blank - 3
        new_state: list = copy(node.state)
        new_state[current_index_blank], new_state[swap_index] = new_state[swap_index], new_state[current_index_blank]
        new_node = Node(node, new_depth, new_state)
        new_children.append(new_node)
    if(Move.RIGHT in moves):
        swap_index = current_index_blank + 1
        new_state: list = copy(node.state)
        new_state[current_index_blank], new_state[swap_index] = new_state[swap_index], new_state[current_index_blank]
        new_node = Node(node, new_depth, new_state)
        new_children.append(new_node)
    if(Move.LEFT in moves):
        swap_index = current_index_blank - 1
        new_state: list = copy(node.state)
        new_state[current_index_blank], new_state[swap_index] = new_state[swap_index], new_state[current_index_blank]
        new_node = Node(node, new_depth, new_state)
        new_children.append(new_node)
        
    return new_children
    

def goal_state_achieved(state):
    return goal_node.state == state

# Heuristics
def hamming(current_node):
    heuristic = 0
    current_index = 0
    for value in current_node.state:
        if value == 'B':
            current_index += 1
            continue
        if goal_node.state.index(value) != current_index:
            heuristic += 1
        current_index += 1
    current_node.heuristic = heuristic

def manhattan(current_node):
    heuristic = 0 
    current_index = 0
    for value in current_node.state:
        if value == 'B':
            current_index += 1
            continue
        goal_index = goal_node.state.index(value)
        row_difference = abs(int(current_index / 3) - int(goal_index / 3))
        col_difference = abs((current_index % 3) - (goal_index % 3))
        heuristic += (row_difference + col_difference)
        current_index += 1
    print(heuristic)
    current_node.heuristic = heuristic

def permutation_inversion(current_node):
    heuristic = 0
    current_index = 0
    for value in current_node.state:
        value_heuristic = 0
        if value == 'B':
            current_index += 1
            continue
        goal_index = goal_node.state.index(value)
        for i in range(0, goal_index+1):
            if(goal_node.state[i] == 'B'):
                continue
            heuristic_index = current_node.state.index(goal_node.state[i])
            if(heuristic_index > current_index):
                value_heuristic += 1
        heuristic += value_heuristic
        current_index += 1
    current_node.heuristic = heuristic

def nilsson(current_node):
    # Set heuristic to manhattan value and then add nilsson sequence
    manhattan(current_node)
    print(current_node.heuristic)
    current_index = 0
    heuristic = 0
    index_clockwise = [0, 1, 2, 5, 8, 7, 6, 3]
    for value in current_node.state:
        if value == 'B':
            current_index += 1
            continue
        if current_index == 4:
            # In Center
            heuristic += 3
        else:
            clockwise_next_index = index_clockwise[(index_clockwise.index(current_index) + 1) % len(index_clockwise)]
            clockwise_value = current_node.state[clockwise_next_index]
            if clockwise_value != goal_node.state[clockwise_next_index]:
                heuristic += 6
        current_index += 1

    # Add to manhattan distance
    current_node.heuristic += heuristic

# Search Algorithms 
def dfs():
    path_length = 0
    while(len(open) > 0):
        current_node = open.pop(0)
        if goal_state_achieved(current_node.state):
            print("Goal State Achieved")
            print('=======================')
            print('Path Length: ' + str(path_length))
            open.clear()
            closed.clear()
            return current_node
        else:
            children = generate_children(current_node)
            closed.append(current_node)
            for child in children:
                is_open = False
                is_closed = False
                for open_node in open:
                    if open_node.state == child.state:
                        is_open = True
                        break
                for close_node in closed:
                    if close_node.state == child.state:
                        is_closed = True
                        break
                if not is_closed and not is_open:
                    open.insert(0, child)
        path_length += 1
    print("Goal State not possible")
    return False

def bfs():
    path_length = 0
    while(len(open) > 0):
        current_node = open.pop(0)
        if goal_state_achieved(current_node.state):
            print("Goal State Achieved")
            print('=======================')
            print('Path Length: ' + str(path_length))
            open.clear()
            closed.clear()
            return current_node
        else:
            children = generate_children(current_node)
            closed.append(current_node)
            for child in children:
                is_open = False
                is_closed = False
                for open_node in open:
                    if open_node.state == child.state:
                        is_open = True
                        break
                for close_node in closed:
                    if close_node.state == child.state:
                        is_closed = True
                        break
                if not is_closed and not is_open:
                    open.append(child)
        path_length += 1
    print("Goal State not possible")
    return False

def best(heuristic):
    path_length = 0
    while(len(open) > 0):
        current_node = open.pop(0)
        if goal_state_achieved(current_node.state):
            print("Goal State Achieved")
            print('=======================')
            print('Path Length: ' + str(path_length))
            open.clear()
            closed.clear()
            return current_node
        else:
            children = generate_children(current_node)
            closed.append(current_node)
            for child in children:
                is_open = False
                is_closed = False
                for open_node in open:
                    if open_node.state == child.state:
                        is_open = True
                        break
                for close_node in closed:
                    if close_node.state == child.state:
                        is_closed = True
                        break
                if not is_closed and not is_open:
                    heuristic(child)
                    index = 0
                    for node in open:
                        if node.heuristic < child.heuristic:
                            index += 1
                            continue
                        else:
                            break
                    open.insert(index, child)
        path_length += 1
    print("Goal State not possible")
    return False

def a_star(heuristic, optimal = False):
    path_length = 0
    while(len(open) > 0):
        current_node = open.pop(0)
        if goal_state_achieved(current_node.state):
            if(not optimal):
                print("Goal State Achieved")
                print('=======================')
                print('Path Length: ' + str(path_length))
            else:
                print('Optimal Path Length (A* with Manhattan Heuristic): ' + str(path_length))
                print('=======================')
            open.clear()
            closed.clear()
            return current_node
        else:
            children = generate_children(current_node)
            closed.append(current_node)
            for child in children:
                is_open = False
                is_closed = False
                for open_node in open:
                    if open_node.state == child.state:
                        is_open = True
                        break
                for close_node in closed:
                    if close_node.state == child.state:
                        is_closed = True
                        break
                if not is_closed and not is_open:
                    heuristic(child)
                    index = 0
                    for node in open:
                        if (node.heuristic + node.depth) < (child.heuristic + child.depth):
                            index += 1
                            continue
                        else:
                            break
                    open.insert(index, child)
        path_length += 1
    print("Goal State not possible")
    return False

if __name__ =='__main__' :
    nilsson(test_node)
    print(test_node.heuristic)
    # search = input('Enter Search Name (bfs, dfs, best, a_star): ')
    # while search not in ['bfs', 'dfs', 'best', 'a_star']:
    #     print('Function Does Not Exist')
    #     search = input('Enter Search Name (bfs, dfs, best, a_star): ')
    
    # if search in ['best', 'a_star']:
    #     user_heuristic = input('Enter Heuristic Name (manhattan, hamming, permutation_inversion): ')
    #     while user_heuristic not in ['manhattan', 'hamming', 'permutation_inversion']:
    #         print('Function Does Not Exist')
    #         user_heuristic = input('Enter Heuristic Name (manhattan, hamming, permutation_inversion): ')
    # confirmed = False
    # while(not confirmed):
    #     print('Enter in following order the state of the initial puzzle: ')
    #     print('1 2 3')
    #     print('4 5 6')
    #     print('7 8 B')
    #     test_state = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    #     count = 0
    #     while count < 9:
    #         print('Current Board: ')
    #         display_board(test_state)
    #         num = str(input('Enter number or B at index(' + str(count) + '): '))
    #         while num not in ['1', '2', '3', '4', '5', '6', '7', '8', 'B'] or num in test_state:
    #             print('Input already in puzzle or not a valid input')
    #             print('Current Board: ')
    #             display_board(test_state)
    #             num = str(input('Enter number or B at index(' + str(count) + '): '))
    #         test_state[count] = num
    #         count += 1
        
    #     print('Current Board: ')
    #     display_board(test_state)
    #     confirm = input('Confirm (y, n): ')
    #     if confirm == 'y':
    #         confirmed = True

    # open.append(Node(None, 0, test_state))

    # if search in ['best', 'a_star']:
    #     solution = locals()[search](locals()[user_heuristic])
    # else:
    #     solution = locals()[search]()

    # if solution:
    #     open.append(test_node)
    #     optimal = a_star(manhattan, True)
    #     display_board(solution.state)

    