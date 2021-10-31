from copy import deepcopy


class Node:
    def __init__(self, board):
        self.board = board
        self.parent = None
        self.move = ""
        self.g = 0
        self.h = 0


class PuzzlesSolver:
    def __init__(self):
        self.initial_state = []
        self.goal_state = []
        self.expanded_states = []
        self.viewed_boards = []
        self.front_boards = []
        self.front_states = []

    def read_file(self):
        print("Type the input file name: (example: input1.txt)")
        file = input()
        f = open(file, "r")
        for i in range(7):
            # read the first three lines for initial state
            if i < 3:
                self.initial_state.append(f.readline().strip("\n").split(" "))
            # read the last 5-7 lines for goal state
            elif i > 3:
                self.goal_state.append(f.readline().strip("\n").split(" "))
            else:
                f.readline()  # skip line 4
        f.close()

    def find_index(self, num):
        for r in range(3):
            for c in range(4):
                if self.goal_state[r][c] == num:
                    return [r, c]

    def h(self, board):
        # sum manhattan distance for all the tiles to the goal
        distance = 0
        for r in range(3):
            for c in range(4):
                goal = self.find_index(board[r][c])
                distance += (abs(r - goal[0]) + abs(c - goal[1]))
        return distance

    def expand(self, node):
        # update the lists
        self.expanded_states.append(node)
        self.viewed_boards.append(node.board)
        self.front_states.remove(node.board)
        self.front_boards.remove(node)

        cost = node.g + 1
        output = []
        board = deepcopy(node.board)

        row = -1
        col = -1
        for r in range(3):
            for c in range(4):
                if board[r][c] == "0":
                    row = r
                    col = c

        if col != 3:
            board[row][col], board[row][col + 1] = board[row][col + 1], board[row][col]  # move left
            left = deepcopy(board)
            if left not in self.viewed_boards:  # check repeated state
                # create node and update
                left_node = Node(left)
                left_node.parent = node
                left_node.g = cost
                left_node.h = self.h(left)
                left_node.move = "L"
                output.append(left_node)
                self.front_boards.append(left_node)
                self.front_states.append(left)
            board[row][col], board[row][col + 1] = board[row][col + 1], board[row][col]  # restore board

        if col != 0:
            board[row][col], board[row][col - 1] = board[row][col - 1], board[row][col]  # move right
            right = deepcopy(board)
            if right not in self.viewed_boards:  # check repeated state
                # create node and update
                right_node = Node(right)
                right_node.parent = node
                right_node.g = cost
                right_node.h = self.h(right)
                right_node.move = "R"
                output.append(right_node)
                self.front_boards.append(right_node)
                self.front_states.append(right)
            board[row][col], board[row][col - 1] = board[row][col - 1], board[row][col]  # restore board

        if row != 2:
            board[row][col], board[row + 1][col] = board[row + 1][col], board[row][col]  # move up
            up = deepcopy(board)
            if up not in self.viewed_boards:  # check repeated state
                # create node and update
                up_node = Node(up)
                up_node.parent = node
                up_node.g = cost
                up_node.h = self.h(up)
                output.append(up_node)
                up_node.move = "U"
                self.front_boards.append(up_node)
                self.front_states.append(up)
            board[row][col], board[row + 1][col] = board[row + 1][col], board[row][col]  # restore board

        if row != 0:
            board[row][col], board[row - 1][col] = board[row - 1][col], board[row][col]  # move down
            down = deepcopy(board)
            if down not in self.viewed_boards:  # check repeated state
                # create node and update
                down_node = Node(down)
                down_node.parent = node
                down_node.g = cost
                down_node.h = self.h(down)
                down_node.move = "D"
                output.append(down_node)
                self.front_boards.append(down_node)
                self.front_states.append(down)
            board[row][col], board[row - 1][col] = board[row - 1][col], board[row][col]  # restore board

    def smallest_f_index(self):

        smallest_f = 999999999
        index = -1

        for i in range(len(self.front_boards)):
            f = self.front_boards[i].g + self.front_boards[i].h
            if f < smallest_f:
                smallest_f = f
                index = i
        return index  # index of the smallest f value in front_board

    def a_star_search(self, initial, goal):
        # initialize
        initial_node = Node(initial)
        initial_node.h = self.h(initial)
        self.front_boards.append(initial_node)
        self.front_states.append(initial)
        self.expand(initial_node)

        while goal not in self.front_states:
            self.expand(self.front_boards[self.smallest_f_index()])  # expand the node with lowest f
            if goal in self.front_states:  # check if goal node is found
                index = self.front_states.index(goal)
                goal_node = self.front_boards[index]
                return goal_node

    def solve(self):
        self.read_file()
        goal_node = self.a_star_search(self.initial_state, self.goal_state)
        f = open("output.txt", 'w')
        print("output: ")
        for r in range(3):  # print initial state
            line = ""
            for c in range(4):
                line += self.initial_state[r][c] + " "
            print(line)
            f.write(line)
            f.write("\n")
        print()
        f.write("\n")
        for r in range(3):  # print goal state
            line = ""
            for c in range(4):
                line += self.goal_state[r][c] + " "
            print(line)
            f.write(line)
            f.write("\n")
        print()
        f.write("\n")
        print(str(goal_node.g))  # level number
        f.write(str(goal_node.g))
        f.write("\n")
        print(str(len(self.expanded_states) + len(self.front_boards)))
        f.write(str(len(self.expanded_states) + len(self.front_boards)))
        f.write("\n")
        path = ""
        fn = ""
        node = goal_node
        while node.parent:
            path = node.move + " " + path  # generate path
            fn = str(node.g + node.h) + " " + fn  # generate fn
            node = node.parent
        print(path)
        f.write(path)
        print(fn)
        f.write("\n")
        f.write(fn)
        f.close()


if __name__ == '__main__':
    solver = PuzzlesSolver()
    solver.solve()
