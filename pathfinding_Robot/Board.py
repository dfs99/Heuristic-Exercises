import copy
import random
import math


class Board:
    """
    The class board will be used as a data structure in order to depict the problem.
    Therefore, each instance will be a node for the graph in order to find the optimal
    solution.
    Positions of the board start form 0 to n-1 for both coordinates.
    """

    def __init__(self, size_x, size_y, robot, goal):
        """
        Though both the size x and y are params, it's needed to define de walls for
        the board's edges to limit the robot.

        :param size_x:
        :param size_y:
        :param robot:
        :param goal: tuple which contains the goal to be set in the board.
        """

        self._given_size_x = size_x
        self._given_size_y = size_y
        self._current_robot = copy.deepcopy(robot)
        self._current_map = []
        self._goal = goal
        # in order to search in the tree.
        self._g_cost = 0
        self._heuristic_cost = 0
        self._total_f_cost = 0
        # parent reference.
        self._parent = None

    @property
    def current_map(self):
        return self._current_map

    @current_map.setter
    def current_map(self, total_size):

        total_size_x = total_size[0] + 2
        total_size_y = total_size[1] + 2

        for i in range(total_size_x):
            aux_list = []
            for j in range(total_size_y):
                # append a row of all walls at the beginning and at the end.
                if i == 0 or (i == total_size_x - 1) or j == 0 or j == (total_size_y - 1):
                    aux_list.append('X')
                else:
                    aux_list.append('_')
            self._current_map.append(aux_list)

    @property
    def given_pos_x(self):
        return self._given_size_x

    @property
    def given_pos_y(self):
        return self._given_size_y

    @property
    def current_robot(self):
        return self._current_robot

    @current_robot.setter
    def current_robot(self, robot):
        self._current_robot = copy.deepcopy(robot)

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, new_goal):
        self._goal = new_goal

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        self._parent = new_parent

    @property
    def g_cost(self):
        return self._g_cost

    @g_cost.setter
    def g_cost(self, new_cost):
        self._g_cost += new_cost

    @property
    def total_f_cost(self):
        return self._total_f_cost

    def set_total_f_cost(self):
        self._total_f_cost = self.heuristic_cost + self.g_cost

    @property
    def heuristic_cost(self):
        return self._heuristic_cost

    @heuristic_cost.setter
    def heuristic_cost(self, value):
        """
        Depending on the value, an heuristic will be executed.
        :param value: 1 means manhattan distance.
                      2 means euclidean distance.
        :return: nothing.
        """
        if value == 1:
            self._heuristic_cost = abs(self.goal[0]-self.current_robot.x) + abs(self.goal[1]-self.current_robot.y)
        elif value == 2:
            self._heuristic_cost = int(math.sqrt((self.goal[0]-self.current_robot.x)**2 +
                                             (self.goal[1]-self.current_robot.y)**2))

    def check_goal(self):
        if self._goal[0] < 0 or self._goal[1] < 0 or self._goal[0] > self.given_pos_x or \
                self._goal[1] > self.given_pos_y:
            print("Invalid Goal")
            return False
        return True

    def place_current_robot(self):

        # check whether the position is valid.
        if self.current_robot.x > self.given_pos_x or self.current_robot.y > self.given_pos_y:
            print("ERROR INVALID POSITION")
        elif self.current_robot.x <= 0 or self.current_robot.y <= 0:
            print("No negative values are valid")
        else:
            # place the robot
            self._current_map[self.current_robot.x][self.current_robot.y] = self.current_robot.represent_robot

    def place_goal(self):
        if self.check_goal():
            self._current_map[(self.goal[0])][self.goal[1]] = 'G'

    def place_obstacles(self):
        """
        The obstacles will be placed right after the goal and robot have taken place.
        They will be placed randomly and in different positions in order not to match with
        the current goal and robot.
        The total number of obstacles will be the maximum of the x size or y size.
        """
        total_amount = max(self.given_pos_x, self.given_pos_y)
        while total_amount != 0:
            x = random.randint(1, self.given_pos_x)
            y = random.randint(1, self.given_pos_y)
            # not to place at robot or goal position
            if x != self.current_robot.x and x != self.goal[0] and y != self.current_robot.y and self.goal[1]:
                self._current_map[x][y] = 'X'
                total_amount -= 1

    def print_board(self):
        """
        The functions prints out the board in order to show the position
        of all the elements involved.
        :return:
        """
        for i in range(len(self._current_map)):
            for j in range(len(self._current_map[i])):
                print(self._current_map[i][j], end="")
            print()

    def check_final_node(self):
        """
        The node will be a final state if the positions of the robot and goal match.
        :return: True if both robot and goal positions are equal
        """
        return True if self.current_robot.x == self.goal[0] and self.current_robot.y == self.goal[1] else False

    def check_operators(self):
        """
        Operators will be checked in this order: 'TOP', 'DOWN', 'LEFT', 'RIGHT'. Therefore,
        a boolean list will be returned with the possible actions the robot can make in order to
        achieve the goal.
        :return: a boolean list which contains all the possible actions in order to generate all the children.
        """
        operators = ['TOP', 'DOWN', 'LEFT', 'RIGHT']
        boolean_operators = []
        for operator in operators:
            if operator == 'TOP':
                # check if the cell above the robot is empty --> '_'
                self.check_top_operator(boolean_operators)
                # Check if the cell bellow the robot is empty.
                self.check_down_operator(boolean_operators)
                # Check if the cell placed at the left of the robot is empty.
                self.check_left_operator(boolean_operators)
                # Check if the cell placed at the right of the robot is empty.
                self.check_right_operator(boolean_operators)
        return boolean_operators

    def check_top_operator(self, boolean_list):
        """
        check if the cell above the robot is empty --> '_' or it contains the solution.
        :param boolean_list: It will be appended True if the cell is empty, otherwise false.
        :return: nothing.
        """
        if self._current_map[self.current_robot.x - 1][self.current_robot.y] == '_' or \
                self._current_map[self.current_robot.x - 1][self.current_robot.y] == 'G':
            boolean_list.append(True)
        else:
            boolean_list.append(False)

    def check_down_operator(self, boolean_list):
        """
        check if the cell down the robot is empty --> '_' or it contains the solution.
        :param boolean_list: It will be appended True if the cell is empty, otherwise false.
        :return: nothing.
        """
        if self._current_map[self.current_robot.x + 1][self.current_robot.y] == '_' or \
                self._current_map[self.current_robot.x + 1][self.current_robot.y] == 'G':
            boolean_list.append(True)
        else:
            boolean_list.append(False)

    def check_left_operator(self, boolean_list):
        """
        check if the cell placed at the left of the robot is empty --> '_' or it contains the solution.
        :param boolean_list: It will be appended True if the cell is empty, otherwise false.
        :return: nothing.
        """
        if self._current_map[self.current_robot.x][self.current_robot.y - 1] == '_' or \
                self._current_map[self.current_robot.x][self.current_robot.y - 1] == 'G':
            boolean_list.append(True)
        else:
            boolean_list.append(False)

    def check_right_operator(self, boolean_list):
        """
        check if the cell placed at the right of the robot is empty --> '_' or it contains the solution.
        :param boolean_list: It will be appended True if the cell is empty, otherwise false.
        :return: nothing.
        """
        if self._current_map[self.current_robot.x][self.current_robot.y + 1] == '_' or \
                self._current_map[self.current_robot.x][self.current_robot.y + 1] == 'G':
            boolean_list.append(True)
        else:
            boolean_list.append(False)

    def generate_successors(self):
        # list that contains all the following successors.
        children = []
        # check all the available possible actions.
        # the following order was used in this function to generate all the possible cases:
        # 'TOP', 'DOWN', 'LEFT', 'RIGHT'
        available_actions = self.check_operators()
        for i in range(len(available_actions)):

            # TOP child
            if i == 0 and available_actions[i]:
                # create another node for the movement TOP.
                # copy the parent node, set the reference to it.
                # change the operator
                child = copy.deepcopy(self)
                # set the new parent.
                child.parent = self
                # plus 1 in the f cost.
                child.g_cost = 1
                # heuristic function.
                child.heuristic_cost = 2
                # calculate the total cost associated.
                child.set_total_f_cost()
                # update the robot.
                child.current_robot.operator_selected = "TOP"
                child.current_robot.x = -1
                # update robot in the map
                child.place_current_robot()
                # append the child to the children list.
                children.append(child)

            # DOWN child
            if i == 1 and available_actions[i]:
                # create another node for the movement TOP.
                # copy the parent node, set the reference to it.
                # change the operator
                child = copy.deepcopy(self)
                # set the new parent.
                child.parent = self
                # plus 1 in the f cost.
                child.g_cost = 1
                # heuristic function.
                child.heuristic_cost = 2
                # calculate the total cost associated.
                child.set_total_f_cost()
                # update the robot.
                child.current_robot.operator_selected = "DOWN"
                child.current_robot.x = 1
                # update robot in the map
                child.place_current_robot()
                # append the child to the children list.
                children.append(child)

            # LEFT child
            if i == 2 and available_actions[i]:
                # create another node for the movement TOP.
                # copy the parent node, set the reference to it.
                # change the operator
                child = copy.deepcopy(self)
                # set the new parent.
                child.parent = self
                # plus 1 in the f cost.
                child.g_cost = 1
                # heuristic function.
                child.heuristic_cost = 2
                # calculate the total cost associated.
                child.set_total_f_cost()
                # update the robot.
                child.current_robot.operator_selected = "LEFT"
                child.current_robot.y = -1
                # update robot in the map
                child.place_current_robot()
                # append the child to the children list.
                children.append(child)

            # RIGHT child
            if i == 3 and available_actions[i]:
                # create another node for the movement TOP.
                # copy the parent node, set the reference to it.
                # change the operator
                child = copy.deepcopy(self)
                # set the new parent.
                child.parent = self
                # plus 1 in the f cost.
                child.g_cost = 1
                # heuristic function.
                child.heuristic_cost = 2
                # calculate the total cost associated.
                child.set_total_f_cost()
                # update the robot.
                child.current_robot.operator_selected = "RIGHT"
                child.current_robot.y = 1
                # update robot in the map
                child.place_current_robot()
                # append the child to the children list.
                children.append(child)

        return children

    def __eq__(self, other):
        if isinstance(other, Board):
            # The instance belongs to Board class.
            # check whether both nodes are equal. Thus, we must compare the Robot's position in order to assure
            # both nodes are Equal.
            return True if self.current_robot.x == other.current_robot.x and \
                self.current_robot.y == other.current_robot.y else False
        else:
            # ERROR
            exit(-1)

    def __hash__(self):
        """
        In order to be able to create a dictionary of nodes the class must be hashable.
        :return: The current instance board id which will be unique.
        """
        return id(self)

    def __str__(self):
        item = "="*50 + "\n" + "NODE FEATURES:\n" + "\nROBOT POS_X: " + \
               str(self.current_robot.x) + "\nROBOT POS_Y: " + str(self.current_robot.y) + "\nACTION: " + \
                str(self.current_robot.operator_selected) + "\nG_cost: " + str(self.g_cost) + "\nHeuristic: " + \
                str(self._heuristic_cost) + "\nTotal Cost: " + str(self.total_f_cost) + "\n" + "="*50 + "\n"
        return item
