import json
import heapq


# A Star Search implementation
class Search(object):
    def __init__(self, board, initial_position):
        self.board = board
        self.position = (initial_position[0], initial_position[1])
        self.actions = []
        # TODO: FILL IN YOUR MATRICULATION NUMBER (AXXXXXXXX) HERE
        self.matric_num = "A0123456Z"
        """
        Constants that you will need to infer the state of the board.
        """
        self.PASSAGE = 0  # any plain cell that a player can pass through
        self.RIGID_WALL = 1  # a wall that cannot be passed through or bombed
        self.PLAYER = 10  # the agent
        self.GOAL_ITEM = 6  # the goal item that will mark the end of the game

        """
        Actions that you will need to include in your returned list object.
        """
        self.UP = 1
        self.DOWN = 2
        self.LEFT = 3
        self.RIGHT = 4

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
        If there are multiple goal items, compute the sequence of actions required for agent to pass through all goal items.

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
        board = self.board

        while (self.find_goal_position(board) != (-1, -1)):
            goal_position = self.find_goal_position(board)
            self.astar_search(board, self.position, goal_position)

        return self.actions

    # performs A star search with manhattan distance heuristic
    def astar_search(self, board, initial_position, goal_position):
        # define every node to be a tuple with the following structure: (path cost + heuristic cost, (position, actions taken))
        frontier = []
        frontier_coordinates = set()
        expanded = set()
        minimum_cost_by_position = dict()
        heapq.heappush(frontier, (0 + self.get_manhattan_distance(initial_position,
                                                                  goal_position), (initial_position, [])))
        frontier_coordinates.add(initial_position)

        while len(frontier) != 0:
            node = heapq.heappop(frontier)
            node_position = node[1][0]
            frontier_coordinates.remove(node_position)
            node_path = node[1][1]
            node_path_cost = len(node_path)  # every action has uniform cost
            node_total_cost = node[0]

            if (minimum_cost_by_position.__contains__(node_position) and
                    minimum_cost_by_position.get(node_position) < node_total_cost):
                # this is a non-optimal copy of this node position so skip it (lazy deletion)
                continue
            else:
                minimum_cost_by_position[node_position] = node_total_cost

            if (self.is_goal(node_position, goal_position)):
                self.actions = self.actions + node_path
                self.position = node_position
                self.board[node_position] = self.PASSAGE
                break

            expanded.add(node_position)

            children = self.generate_valid_children_positions(
                node_position, board)

            for action_to_get_child in list(children.keys()):
                action = action_to_get_child
                new_path = node_path.copy()
                new_path.append(action)
                child_position = children.get(action)
                child_path_cost = node_path_cost + 1
                child_heuristic_cost = self.get_manhattan_distance(
                    child_position, goal_position)
                child_total_cost = child_path_cost + child_heuristic_cost
                child_node = (child_total_cost,
                              (child_position, new_path))
                if (child_position not in frontier_coordinates and child_position not in expanded):
                    frontier_coordinates.add(child_position)
                    heapq.heappush(frontier, child_node)

    # gets manhattan distance between current position and goal position
    def get_manhattan_distance(self, curr_position, goal_position):
        # Problem relaxation: Assumes goal can be reached if there were no walls
        # This makes heuristic admissible
        if (curr_position == goal_position):
            return 0
        else:
            num_horizontal_moves = abs(goal_position[1] - curr_position[1])
            num_vertical_moves = abs(goal_position[0] - curr_position[0])
            # scale up heuristic to help with tie breakers, without blatantly breaking admissibility
            return (num_horizontal_moves + num_vertical_moves) * (1 + 1/100)

    # generates valid successor nodes of current position
    def generate_valid_children_positions(self, position, board):
        children_positions = dict()
        curr_row = position[0]
        curr_col = position[1]

        # Consider Up
        if (curr_row > 0 and board[curr_row - 1, curr_col] != self.RIGID_WALL):
            children_positions[self.UP] = (curr_row - 1, curr_col)
        # Consider Down
        if (curr_row < len(board) - 1 and board[curr_row + 1, curr_col] != self.RIGID_WALL):
            children_positions[self.DOWN] = (curr_row + 1, curr_col)
        # Consider Left
        if (curr_col > 0 and board[curr_row, curr_col - 1] != self.RIGID_WALL):
            children_positions[self.LEFT] = (curr_row, curr_col - 1)
        # Consider Right
        if (curr_col < len(board[0]) - 1 and board[curr_row, curr_col + 1] != self.RIGID_WALL):
            children_positions[self.RIGHT] = (curr_row, curr_col + 1)

        return children_positions

    # determines if a position is a goal position
    def is_goal(self, position, goal_position):
        return position == goal_position

    # finds goal position from board matrix
    def find_goal_position(self, board):
        all_goal_positions = []

        # process 2d list
        for y in range(len(board)):
            for x in range(len(board[0])):
                if(board[y][x] == self.GOAL_ITEM):
                    all_goal_positions.append((y, x))

        if (len(all_goal_positions) == 0):
            # signals end of search
            return (-1, -1)

        curr_position = self.position

        manhattan_distance_from_agent_position = list(map(
            lambda pos: self.get_manhattan_distance(curr_position, pos), all_goal_positions))
        nearest_goal_index = manhattan_distance_from_agent_position.index(
            min(manhattan_distance_from_agent_position))

        return all_goal_positions[nearest_goal_index]

    # You may add more helper methods but do ensure the driver function returns the list of valid integer actions
    # Also make sure you fill up your Matric Number in the init method of this file
