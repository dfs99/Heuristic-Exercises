from copy import deepcopy

"""
    *
    *   Author: Diego Fernandez Sebastian
    *
    *   Script that implements the hanoi towers in a heuristic way.
    *   Thus, an heuristic has been sought in order to be feasible with the aim
    *   to use the A* algorithm to get the solution.
    *
    *   Rules for the game:
    *       1-.) Only one disc must be moved at a time
    *       2-.) Every disc must be associated with a stack. For the implementation only 3 stacks
    *            will be used.
    *       3-.) It's forbidden to place a disc above another if its radius is bigger.
    *

"""


def sort_nodes(node):
    return node.f


def a_star_algorithm():
    # create the first node --> initial node
    discs = [1, 2, 3, 4, 5, 6, 7]
    # discs = [1, 2, 3]
    # where 1 is the smallest one, thus it's above all and 8 is the biggest one
    # and it's underneath every disc.

    initial_node = Node(0, 0, discs)
    initial_node.perform_costs()

    # create the open and closed lists.
    open_list = []
    closed_list = {}

    # add the first node to the open list.
    open_list.append(initial_node)

    # total number of expanded nodes.
    total_expanded_nodes = 0

    while len(open_list) > 0:
        worse = False
        # get the first element from the open list
        current_node = open_list.pop(0)

        # check whether it's the final node.
        if current_node.check_final_state():
            # the final node has been found.
            # print out the total number of expanded nodes.
            print("*" * 30, '\n', "total number of expanded nodes: ", total_expanded_nodes, '\n', "*" * 30)
            # it's path must be returned.
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]

        # check whether the node has been expanded
        for node in closed_list:
            if current_node.__eq__(node):
                # check whether the f cost is better.
                if current_node.f < closed_list[node]:
                    # delete the node in the closed list
                    # add the current node to the closed list
                    # and expand it.
                    break
                else:
                    # Do not expand the node
                    worse = True
                    break

        if worse is False:
            # Add the node to the closed list.
            closed_list[current_node] = current_node.f
            total_expanded_nodes += 1

            # generate successors
            children = current_node.get_successors()

            # append every child to the open list.
            for child in children:
                open_list.append(child)

            # sort the open list.
            open_list.sort(key=sort_nodes)
    # no solution found.
    print(total_expanded_nodes)
    return None


class Node:

    def __init__(self, g, h, discs):
        """
        Node instance will be used as states for the problem.
        """

        self._stack1 = discs
        self._stack2 = []
        self._stack3 = []

        self._g = g
        self._h = h
        self._f = g + h
        self._parent = None

    def set_costs(self):
        if self.check_initial_state():
            self._g = 0
        else:
            self._g += 1

    def set_heuristic(self):
        if self.check_final_state():
            self._h = 0
        else:
            if len(self._stack1) > 0:
                self._h = (2*len(self._stack1) - 1) + len(self._stack2)
            else:
                self._h = len(self._stack2)

    def set_total_costs(self):
        self._f = self._h + self._g

    @property
    def f(self):
        return self._f

    @property
    def parent(self):
        return self._parent

    @property
    def g(self):
        return self._g

    @property
    def h(self):
        return self._h

    def perform_costs(self):
        """
        It calculates all the functions for the current node.
        """
        self.set_costs()
        self.set_heuristic()
        self.set_total_costs()

    def push_disc(self, disc, stack):
        if stack == "stack1":
            self._stack1.insert(0, disc)
        elif stack == "stack2":
            self._stack2.insert(0, disc)
        elif stack == "stack3":
            self._stack3.insert(0, disc)

    def pop_disc(self, stack):
        """
        :param stack:
        :return: The disc popped.
        """
        disc = 0
        if stack == "stack1":
            disc = self._stack1.pop(0)
        elif stack == "stack2":
            disc = self._stack2.pop(0)
        elif stack == "stack3":
            disc = self._stack3.pop(0)

        return disc

    def check_initial_state(self):
        return True if len(self._stack1) == 7 and (len(self._stack2) == 0 and len(self._stack3) == 0) else False

    def check_final_state(self):
        return True if len(self._stack3) == 7 and (len(self._stack1) == 0 and len(self._stack2) == 0) else False

    def __eq__(self, other):
        if isinstance(other, Node):
            # if the stacks are the same both nodes will be equal.
            if (self._stack1 == other._stack1) and (self._stack2 == other._stack2) and (self._stack3 == other._stack3):
                return True
            return False
        else:
            return False

    def __hash__(self):
        return id(self)

    def __str__(self):
        message = "STACK 1 :" + str(self._stack1) + '\n' + "STACK 2 :" + str(self._stack2) + '\n' + \
                  "STACK 3 :" + str(self._stack3)
        return message

    """
    =======================
    CHECK OPERATORS
    =======================
    """

    def check_operators(self):
        # operators = move_disc_S1_S2, move_disc_S1_S3, move_disc_S2_S1, move_disc_S2_S3, move_disc_S3_S1,
        # move_disc_S3_S2
        operators = [self.check_move_disc_s1_s2(), self.check_move_disc_s1_s3(), self.check_move_disc_s2_s1(),
                     self.check_move_disc_s2_s3(), self.check_move_disc_s3_s1(), self.check_move_disc_s3_s2()]

        return operators

    def check_move_disc_s1_s2(self):
        if len(self._stack1) > 0:
            if len(self._stack2) == 0:
                # the disc can be moved without problems.
                return True
            else:
                if self._stack1[0] < self._stack2[0]:
                    return True
                return False
        else:
            return False

    def check_move_disc_s1_s3(self):
        if len(self._stack1) > 0:
            if len(self._stack3) == 0:
                # the disc can be moved without problems.
                return True
            else:
                if self._stack1[0] < self._stack3[0]:
                    return True
                return False
        else:
            return False

    def check_move_disc_s2_s1(self):
        if len(self._stack2) > 0:
            if len(self._stack1) == 0:
                # the disc can be moved without problems.
                return True
            else:
                if self._stack2[0] < self._stack1[0]:
                    return True
                return False
        else:
            return False

    def check_move_disc_s2_s3(self):
        if len(self._stack2) > 0:
            if len(self._stack3) == 0:
                # the disc can be moved without problems.
                return True
            else:
                if self._stack2[0] < self._stack3[0]:
                    return True
                return False
        else:
            return False

    def check_move_disc_s3_s1(self):
        if len(self._stack3) > 0:
            if len(self._stack1) == 0:
                # the disc can be moved without problems.
                return True
            else:
                if self._stack3[0] < self._stack1[0]:
                    return True
                return False
        else:
            return False

    def check_move_disc_s3_s2(self):
        if len(self._stack3) > 0:
            if len(self._stack2) == 0:
                # the disc can be moved without problems.
                return True
            else:
                if self._stack3[0] < self._stack2[0]:
                    return True
                return False
        else:
            return False

    """
    =======================
    GENERATE SUCCESSORS
    =======================
    """

    def get_successors(self):
        operators = self.check_operators()
        children = []
        if operators[0]:
            # from stack 1 to stack 2
            child = deepcopy(self)
            # update the parent
            child._parent = self
            # remove disc from stack 1 to stack 2
            disc = child.pop_disc("stack1")
            child.push_disc(disc, "stack2")
            # add the child
            children.append(child)
            # update the heuristic and overall cost.
            child.perform_costs()

        if operators[1]:
            # from stack 1 to stack 3
            child = deepcopy(self)
            # update the parent
            child._parent = self
            # remove disc from stack 1 to stack 3
            disc = child.pop_disc("stack1")
            child.push_disc(disc, "stack3")
            # add the child
            children.append(child)
            # update the heuristic and overall cost.
            child.perform_costs()

        if operators[2]:
            # from stack 2 to stack 1
            child = deepcopy(self)
            # update the parent
            child._parent = self
            # remove disc from stack 2 to stack 1
            disc = child.pop_disc("stack2")
            child.push_disc(disc, "stack1")
            # add the child
            children.append(child)
            # update the heuristic and overall cost.
            child.perform_costs()

        if operators[3]:
            # from stack 2 to stack 3
            child = deepcopy(self)
            # update the parent
            child._parent = self
            # remove disc from stack 2 to stack 3
            disc = child.pop_disc("stack2")
            child.push_disc(disc, "stack3")
            # add the child
            children.append(child)
            # update the heuristic and overall cost.
            child.perform_costs()

        if operators[4]:
            # from stack 3 to stack 1
            child = deepcopy(self)
            # update the parent
            child._parent = self
            # remove disc from stack 3 to stack 1
            disc = child.pop_disc("stack3")
            child.push_disc(disc, "stack1")
            # add the child
            children.append(child)
            # update the heuristic and overall cost.
            child.perform_costs()

        if operators[5]:
            # from stack 3 to stack 2
            child = deepcopy(self)
            # update the parent
            child._parent = self
            # remove disc from stack 3 to stack 2
            disc = child.pop_disc("stack3")
            child.push_disc(disc, "stack2")
            # add the child
            children.append(child)
            # update the heuristic and overall cost.
            child.perform_costs()

        return children


solution = a_star_algorithm()
if solution is None:
    print("No solution has been found")
else:
    i = 0
    for sol in solution:
        print('*' * 30)
        print()
        print("Step: ", i)
        print(sol)
        print()
        print("g(n)", sol.g)
        print("h(n)", sol.h)
        print("f(n)", sol.f)
        print('*' * 30)
        i += 1
