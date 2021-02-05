import copy
"""
    *
    *   Author: Diego Fernandez Sebastian
    *
    *   Script that aims to solve the N-puzzle problem.
    *
    *   Rules:
    *       1-.) It's possible to move only one token at a time.
    *       2-.) The token must be adjacent to the "unfilled" one
    *       3-.) Tokens are bounded for the board
    *
    *   change the function check_final_configuration() in order to be able to run different configurations
    *   Right now is in 15-Puzzle
    *
"""

# each instance is going to be represented as a list of lists.
source = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
source1 = [[1, 0, 2], [3, 4, 5], [6, 7, 8]]
source2 = [[1, 2, 0], [3, 4, 5], [6, 7, 8]]
source3 = [[1, 2, 5], [3, 4, 8], [6, 0, 7]]
source4 = [[1, 2, 3, 7], [4, 5, 6, 11], [8, 9, 14, 10], [0, 12, 13, 15]]
source5 = [[1, 2, 3, 0], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]

# The algorithm of uninformed search used will be the BFS --> breadth first search
# It grants to find a solution within a specific depth. In this case the depth will be
# the number of steps in order to return to its original shape.
def get_solution1(src):
    # create the queue
    # add the source to the queue
    fifo = [src]

    # count the number of nodes expanded.
    total_n_nodes = 0
    while len(fifo) > 0:
        # get the first element of the list.
        current_node = fifo.pop(0)
        total_n_nodes += 1

        # check whether the first element is the terminal node
        if check_final_configuration(current_node):
            print('=' * 30)
            print_configuration(current_node)
            print('=' * 30)
            print('total expanded nodes', total_n_nodes)
            return current_node

        # get its children
        children = move_tokens(current_node)
        # check whether the terminal node has been expanded.
        for child in children:
            if check_final_configuration(child):
                # print out the configuration.
                # end the function
                print('=' * 30)
                print_configuration(child)
                print('=' * 30)
                print('total expanded nodes', total_n_nodes)
                return child
            # Otherwise, add the child to the fifo queue.
            fifo.append(child)

    # No solution has been found.
    return None


# Due to its number of combinations --> 9!/2 for a 8-puzzle
# A* Algorithm will be used in order to avoid to repeat combinations.
# No heuristic function is used tho.
def get_solution_a_star(src):
    # create the queue
    # add the source to the queue
    open_list = [src]
    closed_list = []
    # count the number of nodes expanded.
    total_n_nodes = 0
    while len(open_list) > 0:
        # get the first element of the list.
        current_node = open_list.pop(0)
        total_n_nodes += 1

        # check whether the first element is the terminal node
        if check_final_configuration(current_node):
            print('=' * 30)
            print_configuration(current_node)
            print('=' * 30)
            print('total expanded nodes', total_n_nodes)
            return current_node

        if current_node in closed_list:
            # check other iteration, it has already be visited and expanded.
            continue
        else:
            # get its children
            children = move_tokens(current_node)
            # check whether the terminal node has been expanded.
            for child in children:
                if check_final_configuration(child):
                    # print out the configuration.
                    # end the function
                    print('=' * 30)
                    print_configuration(child)
                    print('=' * 30)
                    print('total expanded nodes', total_n_nodes)
                    return child
                # Otherwise, add the child to the fifo queue.
                open_list.append(child)

            # append the current node to the closed list.
            closed_list.append(current_node)

    # No solution has been found.
    return None


def check_final_configuration(conf):
    # The terminal node must have this shape. Within this form the configuration is sorted.
    terminal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    terminal1 = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    return True if conf == terminal1 else False


"""
================
    OPERATORS   
================
"""


def move_tokens(token):
    """
    :param: A list is passed in order to create all its children out of the configuration within the list.
    :return: A list contains with all the possibilities expanded.
    """
    # call the function adjacent
    adjacents = adjacent(token)

    # children from the configuration
    all_children = []
    for i in range(len(adjacents)):
        for j in range(len(adjacents[i])):
            # first check whether the "unfilled" token is adjacent to the token passed.
            if adjacents[i][j]:
                # swap positions within the board.
                # search in order to find the space.
                unfilled_posx = 0
                unfilled_posy = 0
                for ii in range(len(token)):
                    for jj in range(len(token[i])):
                        if token[ii][jj] == 0:
                            unfilled_posx = ii
                            unfilled_posy = jj
                            break
                # swap positions.
                # copy the configuration.
                child = copy.deepcopy(token[:])
                # save the token
                t = child[i][j]
                # add the unfilled token.
                child[i][j] = 0
                # add the token in the previous unfilled token position
                child[unfilled_posx][unfilled_posy] = t

                # append the new node.
                all_children.append(child)
            else:
                # The token was not accessible.
                # Thus, the token won't be swapped. Though the loop must continue.
                continue

    # return the children generated
    return all_children


def adjacent(token):
    """

    :param token: The list is passed as parameter in order to check all the adjacent tokens.
    :return: A boolean list is returned with the values checked.
    """
    adjacents = []
    for i in range(0, len(token)):
        adjs = []
        adjacents.append(adjs)
        for j in range(0, len(token[i])):
            # the board has certain boundaries.
            # check the tokens placed in the boundaries. Rows and columns.
            if (i == 0 or i == len(token) - 1) or (j == 0 or j == len(token[i]) - 1):
                # Notice that the tokens placed in the corners are accessed within these conditions as well.
                if (i == 0 or i == len(token) - 1) and (j == 0 or j == len(token[i]) - 1):
                    # check for the corners
                    # upper-left corner
                    if i == j and i + j == 0:
                        if token[i + 1][j] == 0 or token[i][j + 1] == 0:
                            adjs.append(True)
                        else:
                            adjs.append(False)
                    # upper-right corner
                    elif i - j < 0:
                        if token[i + 1][j] == 0 or token[i][j - 1] == 0:
                            adjs.append(True)
                        else:
                            adjs.append(False)
                    # lower-left corner
                    elif i - j > 0:
                        if token[i - 1][j] == 0 or token[i][j + 1] == 0:
                            adjs.append(True)
                        else:
                            adjs.append(False)
                    # lower-right corner
                    elif i == j and i + j != 0:
                        if token[i - 1][j] == 0 or token[i][j - 1] == 0:
                            adjs.append(True)
                        else:
                            adjs.append(False)
                    else:
                        adjs.append(False)

                else:
                    # check for other tokens in the boundaries.
                    if i == 0:
                        if token[i][j + 1] == 0 or token[i][j - 1] == 0 or token[i + 1][j] == 0:
                            adjs.append(True)
                        else:
                            adjs.append(False)
                    elif i == len(token) - 1:
                        if token[i][j + 1] == 0 or token[i][j - 1] == 0 or token[i - 1][j] == 0:
                            adjs.append(True)
                        else:
                            adjs.append(False)
                    elif j == 0:
                        if token[i - 1][j] == 0 or token[i + 1][j] == 0 or token[i][j + 1] == 0:
                            adjs.append(True)
                        else:
                            adjs.append(False)
                    elif j == len(token) - 1:
                        if token[i - 1][j] == 0 or token[i + 1][j] == 0 or token[i][j - 1] == 0:
                            adjs.append(True)
                        else:
                            adjs.append(False)
                    else:
                        adjs.append(False)
            # check the tokens placed in the middle
            elif (0 < i < len(token) - 1) and (0 < j < len(token[i]) - 1):
                if token[i + 1][j] == 0 or token[i - 1][j] == 0 or token[i][j + 1] == 0 or token[i][j - 1] == 0:
                    adjs.append(True)
                else:
                    adjs.append(False)

    return adjacents


def print_configuration(conf):
    for row in conf:
        for elem in row:
            print(elem, end=' ')
        print()


# change the function check_final_configuration() in order to be able to run different configurations
get_solution1(source4)
get_solution_a_star(source4)
