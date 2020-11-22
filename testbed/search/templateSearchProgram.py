import json
class Search(object):
    def __init__(self, board, initial_position):
        self.board = board,
        self.initial_position = initial_position
        # TODO: FILL IN YOUR MATRICULATION NUMBER (AXXXXXXXX) HERE
        self.matric_num = ""
        """
        Constants that you will need to infer the state of the board.
        """
        self.PASSAGE = 0  # any plain cell that a player can pass through
        self.RIGID_WALL = 1  # a wall that cannot be passed through or bombed
        self.PLAYER = 10  # the agent
        self.GOAL_ITEM = 8  # the goal item that will mark the end of the game

        """
        Actions that you will need to include in your returned list object.
        """
        self.UP = 1
        self.DOWN = 2
        self.LEFT = 3
        self.RIGHT = 4

    # driver function that will be called by runner script

    # driver function that will be called by runner script
    def evaluate_search(self, script_name):
        output = {}
        output['actions'] = self.search()

        with open(f'{script_name}.json', 'w') as outfile:
            json.dump(output, outfile)

    # The method to implement
    def search(self):
        """
        Compute the sequence of actions required for agent to move to the cell containing a goal item.

        Useful inputs:
            board:
                - A 2-Dimensional Square Matrix (i.e. width = height)
                - Can have a variable width so ensure your program adapts to different square board sizes
                - The board contains integer values which represent objects that are positioned on that cell.
                For example, if board[y][x] = 2, there is a wooden wall at coordinates (x, y) of the board, i.e.
                the (x + 1)th column and the (y + 1)th row of the board. DO REMEMBER WE ARE USING 0-BASED INDEXING.
                - Refer to constants defined at the top of this file to understand the different object representations.

            initial_position:
                - A 2-tuple (y, x) that corresponds to initial position of agent on the board that corresponds to the (y + 1)th
                row and the (x + 1)th column of the board.

        Returns:
            actions: A list of valid integer actions. Do refer to the definition of valid actions near the top of the file.
        """
        # to extract 2d matrix from class array object
        board = self.board[0]
        pass

        # You may add more helper methods but do ensure the driver function returns the list of valid integer actions
        # Also make sure you fill up your Matric Number in the init method of this file
