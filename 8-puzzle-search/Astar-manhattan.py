import os
import sys
from Queue import PriorityQueue

pq = PriorityQueue()
visited_states = set()


class Puzzle(object):
    """
    A* search with MANHATTAN HEURISTIC
    """
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.cost = 0
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.explored = [0]
        self.explored_tot = 0
        self.num_nodes = [0]
        self.total_prev_h_cost = 0

    def __cmp__(self, other):
        return cmp(self.cost, other.cost)

    def to_int_rep(self):
        return tuple(map(tuple, self.init_state))

    def is_solvable(self):
        """Checks if state is solvable."""
        inversions = 0
        n = len(self.init_state)
        for i in range(n*n):
            x, y = self.get_location_in_goal_state(i+1)
            for j in range(i + 1, n*n):
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

    def solve(self):

        # check solvable
        if self.is_solvable() is not True:
            return ["UNSOLVABLE"], 0

        pq.put(self)
        while pq.qsize() is not 0:
            new_state = pq.get()

            self.explored_tot += 1
            if(len(new_state.actions)) >= len(self.num_nodes):
                self.num_nodes.append(pq.qsize())
            elif self.num_nodes[len(new_state.actions)] < pq.qsize():
                self.num_nodes[len(new_state.actions)] = pq.qsize()

            if (len(new_state.actions)) >= len(self.explored):
                self.explored.append(self.explored_tot)
            elif self.num_nodes[len(new_state.actions)] < self.explored_tot:
                self.num_nodes[len(new_state.actions)] = self.explored_tot

            visited_states.add(new_state.to_int_rep())
            if new_state.init_state == self.goal_state:
                average_h_cost = new_state.total_prev_h_cost / float(len(new_state.actions))
                return new_state.actions, average_h_cost

            #print new_state.f_cost()
            # Actions
            empty_space = new_state.get_empty_space()

            down_res = new_state.move_down(empty_space)
            if down_res is not None and down_res.to_int_rep() not in visited_states:
                down_res.cost = down_res.f_cost()
                pq.put(down_res)

            up_res = new_state.move_up(empty_space)
            if up_res is not None and up_res.to_int_rep() not in visited_states:
                up_res.cost = up_res.f_cost()
                pq.put(up_res)

            left_res = new_state.move_left(empty_space)
            if left_res is not None and left_res.to_int_rep() not in visited_states:
                left_res.cost = left_res.f_cost()
                pq.put(left_res)

            right_res = new_state.move_right(empty_space)
            if right_res is not None and right_res.to_int_rep() not in visited_states:
                right_res.cost = right_res.f_cost()
                pq.put(right_res)

        return ["UNSOLVABLE"], 0

    def f_cost(self):
        return self.h_cost() + len(self.actions)

    def h_cost(self):
        h = 0
        n = len(self.init_state)
        for i in range(n):
            for j in range(n):
                if self.init_state[i][j] != 0:
                    x, y = self.get_location_in_goal_state(self.init_state[i][j])
                    h += abs(x - i) + abs(y - j)
        return h

    def get_empty_space(self):
        n = len(self.init_state)
        for i in range(0, n):
            for j in range(0, n):
                if self.init_state[i][j] == 0:
                    return i, j

    def move_up(self, empty_space):
        n = len(self.init_state)
        if empty_space[0] == n - 1:
            return None
        else:
            new_puzzle = self.copy()

            r = empty_space[0]
            c = empty_space[1]

            new_puzzle.init_state[r][c] = new_puzzle.init_state[r + 1][c]
            new_puzzle.init_state[r + 1][c] = 0

            new_puzzle.actions.append("UP")
            return new_puzzle

    def move_down(self, empty_space):
        if empty_space[0] == 0:
            return None
        else:
            new_puzzle = self.copy()

            r = empty_space[0]
            c = empty_space[1]

            new_puzzle.init_state[r][c] = new_puzzle.init_state[r - 1][c]
            new_puzzle.init_state[r - 1][c] = 0

            new_puzzle.actions.append("DOWN")
            return new_puzzle

    def move_left(self, empty_space):
        n = len(self.init_state)
        if empty_space[1] == n - 1:
            return None
        else:
            new_puzzle = self.copy()

            r = empty_space[0]
            c = empty_space[1]

            new_puzzle.init_state[r][c] = new_puzzle.init_state[r][c + 1]
            new_puzzle.init_state[r][c + 1] = 0

            new_puzzle.actions.append("LEFT")
            return new_puzzle

    def move_right(self, empty_space):
        if empty_space[1] == 0:
            return None
        else:
            new_puzzle = self.copy()

            r = empty_space[0]
            c = empty_space[1]

            new_puzzle.init_state[r][c] = new_puzzle.init_state[r][c - 1]
            new_puzzle.init_state[r][c - 1] = 0

            new_puzzle.actions.append("RIGHT")
            return new_puzzle

    def get_location_in_goal_state(self, num):
        n = len(self.init_state)
        x_loc = (num - 1) / n
        y_loc = (num - 1) % n

        return x_loc, y_loc

    def copy(self):
        new_init_state = self.copy_state()
        new_puzzle = Puzzle(new_init_state, self.goal_state)
        new_puzzle.actions = self.copy_actions()
        new_puzzle.total_prev_h_cost = self.total_prev_h_cost + new_puzzle.h_cost()
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

    i, j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number, base=10)
            if 0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i - 1) // n][(i - 1) % n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans, average_h_cost = puzzle.solve()

    with open(sys.argv[2], 'w') as f:
        for answer in ans:
            f.write(answer + '\n')







