from Board import *
from Robot import *


def set_initial_node():
    # create the robot.
    my_robot = Robot(1, 6)
    # create the board with the goal at 3,3 and the robot.
    my_board = Board(6, 6, my_robot, (6, 1))
    # set the current board.
    my_board.current_map = (my_board.given_pos_x, my_board.given_pos_y)
    # place the robot.
    my_board.place_current_robot()
    # place the goal.
    my_board.place_goal()
    # place obstacles
    my_board.place_obstacles()

    # prints out the board.
    my_board.print_board()
    return my_board


def sort_list(node):
    return node.total_f_cost


def a_star_search():
    # open list
    open_list = []
    # closed list
    closed_list = {}

    # total nodes expanded
    total_nodes_expanded = 0

    # create the very first node.
    root = set_initial_node()
    # append it to the open_list
    open_list.append(root)

    # while the open_list is not empty, this is, the container's length is
    # greater than 0.
    while len(open_list) > 0:

        # pop the first node
        # get the lowest value first.
        current_node = open_list.pop(0)

        # check whether it's the goal
        if current_node.check_final_node():
            # print the total number of nodes.
            print("Total Nodes expanded: ", total_nodes_expanded)
            # the goal has been reached.
            # return the path which will contain all the steps executed.
            path = []
            # loop through in order to get the whole path sought.
            while current_node is not None:
                path.append(current_node)
                # update the reference, backtracking
                current_node = current_node.parent
            # in order to be ordered, the path is returned reversed.
            return path[::-1]

        # aux variable in order to check whether the node was in the closed list or not.
        belongs = False
        # check if the current node is in the closed list or not.
        for node in closed_list:
            if current_node.__eq__(node):
                # both nodes were equal, check which one has better f(n)
                if current_node.total_f_cost < closed_list.get(node):
                    # remove the entry within the closed list
                    del closed_list[node]
                    # add the new entry with the updated f(n)
                    # bellow at belongs = false
                    break
                else:
                    # do not expand a node which has worse f(n), thus continue.
                    # duplicate detection
                    belongs = True
                    break

        if belongs is False:
            total_nodes_expanded += 1
            # The node wasn't in the closed list or it had a better f(n)
            closed_list[current_node] = current_node.total_f_cost

            # generate the successors
            children = current_node.generate_successors()
            for child in children:
                open_list.append(child)

            # sort the list
            open_list.sort(key=sort_list)

    return None


def solution_path(end_node):
    if end_node is None:
        print("NO SOLUTION HAS FOUND")
    else:
        i = 1
        for sol in end_node:
            print(i, "-. ", sol.current_robot)
            i += 1
        print(end_node[-1].print_board())


def hill_climbing_algorithm():
    # this approach may not get the solution
    # The best node heuristically will be expanded, others will be discarded.
    # set the first node.
    node_expanded = set_initial_node()
    total_nodes_expanded = 0
    while node_expanded.check_final_node() is False:
        # expand all the nodes
        children = node_expanded.generate_successors()
        total_nodes_expanded += 1
        # check whether the list is empty or not.
        # if list is empty, the hill-climbing algorithm will have finished without solution
        if len(children) == 0:
            print("No solution has been found using the Hill-Climbing Algorithm")
            return None

        # sort the list.
        children.sort(key=sort_list)
        # extract the first element --> lower heuristic value.
        node_expanded = children.pop(0)
    print("Total Nodes expanded: ", total_nodes_expanded)
    return node_expanded


def beam_search_algorithm(k):
    # K nodes will be expanded simultaneously each iteration
    # k will be a param, though for the example it will be 3 for further trials.

    # create the open list.
    open_list = []
    # total nodes expanded.
    total_nodes_expanded = 0
    # get the root node.
    root = set_initial_node()
    # append it to the open list.
    open_list.append(root)

    while len(open_list) > 0:
        # expand all the nodes from the open_list, this list.
        # list which contains all the children in order to make further evaluations afterwards.
        all_children = []
        # get all the successors of all the elements form the open list.
        for i in range(len(open_list)):
            total_nodes_expanded += 1
            all_children += open_list[i].generate_successors()
            # remove form the open list the node has been expanded.

        # remove all the elements in the list.
        for elem in open_list:
            open_list.remove(elem)

        # check whether the solution is within any child.
        for node in all_children:
            if node.check_final_node() is True:
                # a solution has been found.
                # get through backtracking the solution.
                # the path contains a list with all the nodes from be beginning to the end
                # have been used in order to reach this solution.
                print("Total nodes expanded.: ", total_nodes_expanded)
                path = []
                while node is not None:
                    path.append(node)
                    node = node.parent
                return path[::-1]

        # Only if no solution has been found.
        # sort the list in order to get the best K nodes.
        all_children.sort(key=sort_list)
        # append the first three nodes into the open list.
        if len(all_children) < 3:
            # all all the elements to the list.
            for child in all_children:
                open_list.append(child)
        else:
            # add only 3 elements.
            for i in range(0, k):
                open_list.append(all_children[i])
    # No solution has been found.
    print("No solution has been found using the beam search.")
    return None


print("*"*75)
print("*"*75)
# A* algorithm
solution_path(a_star_search())
print("*"*75)
print("*"*75)
# Hill-Climbing algorithm
solution_hc = hill_climbing_algorithm()
if solution_hc is not None:
    solution_hc.print_board()
print("*"*75)
print("*"*75)
# beam search algorithm
solution_bs = beam_search_algorithm(3)
if solution_bs is not None:
    for step in solution_bs:
        print(step.current_robot)
    # print the board.
    print(solution_bs[-1].print_board())
print("*"*75)
print("*"*75)
