from copy import copy
from node import Move, Node


goal_node = Node(None, -1, ['1', '2', '3', '8', 'B', '4', '7', '6', '5'])
test_node = Node(None, 1, ['B', '1', '3', '8', '2', '4', '7', '6', '5'])

open = list()
closed = list()

def display_board(state):
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


def dfs():
    while(len(open) > 0):
        current_node = open.pop(0)
        if goal_state_achieved(current_node.state):
            print("Goal State Achieved")
            print(current_node.depth)
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
                    
                
        print("Open: " + str(open))
        print("Closed: " + str(closed))
    print("Goal State not possible")
    return False

def bfs():
    while(len(open) > 0):
        current_node = open.pop(0)
        if goal_state_achieved(current_node.state):
            print("Goal State Achieved")
            print(current_node.depth)
            return current_node
        else:
            children = generate_children(current_node)
            closed.append(current_node)
            for child in children:
                if child not in closed and child not in open:
                    open.append(child)
        print("Open: " + str(open))
        print("Closed: " + str(closed))
    print("Goal State not possible")
    return False

def best():
    print('test3')

def a_star():
    print('test4')

if __name__ =='__main__' :
    open.append(test_node)
    solution = dfs()

    test = [Node(None, 1, [['B', '1', '3', '8', '2', '4', '7', '6', '5']])]

    