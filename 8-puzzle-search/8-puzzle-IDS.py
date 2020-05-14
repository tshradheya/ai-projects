import os
import sys

class Puzzle(object):
    explored = 0
    num_nodes = []

    def __init__(self, init_state, goal_state, visited):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.visited = visited

    def solve(self):

        # check solvable
        if self.is_solvable() is not True:
            return ["UNSOLVABLE"]

        return self.IDS()

    def DLS(self, limit, current_level):
        if self.init_state == self.goal_state:
            return self.actions
        if current_level == limit:
            return False

        Puzzle.explored += 1
        self.visited.add(self.to_int_rep())

        up = self.move_up()
        if up.to_int_rep() not in self.visited:
            result = up.DLS(limit, current_level + 1)
            if result != False:
                return result
        down = self.move_down()
        if down.to_int_rep() not in self.visited:
            result = down.DLS(limit, current_level + 1)
            if result != False:
                return result
        left = self.move_left()
        if left.to_int_rep() not in self.visited:
            result = left.DLS(limit, current_level + 1)
            if result != False:
                return result
        right = self.move_right()
        if right.to_int_rep() not in self.visited:
            result = right.DLS(limit, current_level + 1)
            if result != False:
                return result
        return False

    def IDS(self):
        Puzzle.num_nodes.append(0)
        i = 1
        #Check that puzzle is solvable before attempting IDS
        while True:
            # To visualise which level of the IDS we are at
            # print(i)
            result = self.DLS(i, 0)
            Puzzle.num_nodes.append(Puzzle.num_nodes[-1] + (2 ** (i*2)))
            if result != False:
                return result
            i += 1

    def to_int_rep(self):
        return tuple(map(tuple, self.init_state))

    def get_location_in_goal_state(self, num):
        n = len(self.init_state)
        x_loc = (num - 1) / n
        y_loc = (num - 1) % n

        return x_loc, y_loc

    def is_solvable(self):
        """Checks if state is solvable."""
        inversions = 0
        n = len(self.init_state)
        for i in range(n * n):
            x, y = self.get_location_in_goal_state(i+1)
            for j in range(i + 1, n * n):
                x2, y2 = self.get_location_in_goal_state(j+1)
                if self.init_state[x][y] != 0 and self.init_state[x2][y2] != 0 and self.init_state[x2][y2] < self.init_state[x][y]:
                    inversions += 1

        if n % 2 == 1 and inversions % 2 == 0:  # Odd and numberOfInversions is even
            return True

        empty_space = self.get_empty_space()
        if n % 2 == 0 and empty_space[0] % 2 == 0 and inversions % 2 == 1:  # Blank on even row from bottom and inversions odd
            return True
        if n % 2 == 0 and empty_space[0] % 2 == 1 and inversions % 2 == 0:  # Blank on odd row from bottom and inversions even
            return True

        return False

    def get_empty_space(self):
        n = len(self.init_state)
        for i in range(0, n):
            for j in range(0, n):
                if self.init_state[i][j] == 0:
                    return (i, j)
        return (-1, -1)

    def move_up(self):
        n = len(self.init_state)
        empty_space = self.get_empty_space()
        if empty_space[0] == n - 1:
            return self
        else:
            new_puzzle = self.copy()

            r = empty_space[0]
            c = empty_space[1]

            new_puzzle.init_state[r][c] = new_puzzle.init_state[r + 1][c]
            new_puzzle.init_state[r + 1][c] = 0

            new_puzzle.actions.append("UP")
            return new_puzzle

    def move_down(self):
        empty_space = self.get_empty_space()
        if empty_space[0] == 0:
            return self
        else:
            new_puzzle = self.copy()

            r = empty_space[0]
            c = empty_space[1]

            new_puzzle.init_state[r][c] = new_puzzle.init_state[r - 1][c]
            new_puzzle.init_state[r - 1][c] = 0

            new_puzzle.actions.append("DOWN")
            return new_puzzle

    def move_left(self):
        n = len(self.init_state)
        empty_space = self.get_empty_space()
        if empty_space[1] == n - 1:
            return self
        else:
            new_puzzle = self.copy()

            r = empty_space[0]
            c = empty_space[1]

            new_puzzle.init_state[r][c] = new_puzzle.init_state[r][c + 1]
            new_puzzle.init_state[r][c + 1] = 0

            new_puzzle.actions.append("LEFT")
            return new_puzzle

    def move_right(self):
        empty_space = self.get_empty_space()
        if empty_space[1] == 0:
            return self
        else:
            new_puzzle = self.copy()

            r = empty_space[0]
            c = empty_space[1]

            new_puzzle.init_state[r][c] = new_puzzle.init_state[r][c - 1]
            new_puzzle.init_state[r][c - 1] = 0

            new_puzzle.actions.append("RIGHT")
            return new_puzzle

    def copy(self):
        new_init_state = self.copy_state()
        new_puzzle = Puzzle(new_init_state, self.goal_state, self.visited.copy())
        new_puzzle.actions = self.copy_actions()
        return new_puzzle

    def copy_state(self):
        new_state = [[x for x in row] for row in self.init_state]
        return new_state

    def copy_actions(self):
        res = []
        for i in range((len(self.actions))):
            res.append(self.actions[i])
        return res


if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]


    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state, set())

    ans = puzzle.solve()

    with open(sys.argv[2], 'w') as f:
        for answer in ans:
            f.write(answer+'\n')







