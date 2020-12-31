class Robot:

    def __init__(self, pos_x, pos_y):
        """

        :param pos_x: coordinate x in the board.
        :param pos_y: coordinate y in the board.

        Two more attributes are declared within class robot.
        operator_selected will contain the operator/action the robot has taken the current turn.
        represent_robot contains the symbol which will represent the robot in the board.
        """
        self._x = pos_x
        self._y = pos_y
        self._operator_selected = None
        self._represent_robot = 'R'

    @property
    def x(self):
        """

        :return: the coordinate x of the current robot.
        """
        return self._x

    @x.setter
    def x(self, new_x):
        """

        :param new_x: new x coordinate for the robot.
        :return: nothing.
        """
        self._x += new_x

    @property
    def y(self):
        """

        :return: the y coordinate of the current robot.
        """
        return self._y

    @y.setter
    def y(self, new_y):
        """

        :param new_y: new y coordinate for the robot.
        :return: nothing.
        """
        self._y += new_y

    @property
    def represent_robot(self):
        """

        :return: the symbol which represents the robot in the table.
        Typically will be 'R'.
        """
        return self._represent_robot

    @property
    def operator_selected(self):
        return self._operator_selected

    @operator_selected.setter
    def operator_selected(self, new_operator):
        self._operator_selected = new_operator

    def __str__(self):
        message = "Robot position is: x--> " + str(self.x) + " y--> " + str(self.y)
        return message
