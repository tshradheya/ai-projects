import os
import sys
from Queue import PriorityQueue

pq = PriorityQueue()
visited_states = set()


class Puzzle(object):
    """
    A* search with LINEAR CONFLICT HEURISTIC
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

    def solve(self):

        # check solvable
        if self.is_solvable() is not True:
            return ["UNSOLVABLE"], 0

        pq.put((self.f_cost(), self))
        while pq.qsize() is not 0:
            cost, new_state = pq.get()

            self.explored_tot += 1

            if (len(new_state.actions)) >= len(self.num_nodes):
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

            # Actions
            empty_space = new_state.get_empty_space()

            down_res = new_state.move_down(empty_space)
            if down_res is not None and down_res.to_int_rep() not in visited_states:
                down_res.cost = down_res.f_cost()
                pq.put((down_res.cost, down_res))

            up_res = new_state.move_up(empty_space)
            if up_res is not None and up_res.to_int_rep() not in visited_states:
                up_res.cost = up_res.f_cost()
                pq.put((up_res.cost, up_res))

            left_res = new_state.move_left(empty_space)
            if left_res is not None and left_res.to_int_rep() not in visited_states:
                left_res.cost = left_res.f_cost()
                pq.put((left_res.cost, left_res))

            right_res = new_state.move_right(empty_space)
            if right_res is not None and right_res.to_int_rep() not in visited_states:
                right_res.cost = right_res.f_cost()
                pq.put((right_res.cost, right_res))

        return ["UNSOLVABLE"], 0

    def f_cost(self):
        return self.h_cost() + len(self.actions)

    def h_cost(self):
        n = len(self.init_state)
        h = 0
        linearConflict = 0
        for i in range(n):
            for j in range(n):
                num = self.init_state[i][j]
                if num == 0:
                    continue
                location_in_goal = self.get_location_in_goal_state(num)
                h += abs(location_in_goal[0]-i) + abs(location_in_goal[1]-j)

            linearConflict += self.conflict_row_col(i)

        return h + 2 * linearConflict

    def conflict_row_col(self, i):
        n = len(self.init_state)

        c1 = [[]]*n
        for j in range(n):
            c1[j] = []

        c2 = [[]] * n
        for j in range(n):
            c2[j] = []

        # Evaluating all conflicts in row i and column i
        for j in range(n):
            tj1 = self.init_state[i][j]
            tj2 = self.init_state[j][i]
            gr_j1, gc_j1 = self.get_location_in_goal_state(tj1)
            gr_j2, gc_j2 = self.get_location_in_goal_state(tj2)
            flag1 = 1
            flag2 = 1
            if gr_j1 != i or tj1 == 0:
                flag1 = 0
            if gc_j2 != i or tj2 == 0:
                flag2 = 0

            for k in range(n):
                tk1 = self.init_state[i][k]
                tk2 = self.init_state[k][i]
                gr_k1, gc_k1 = self.get_location_in_goal_state(tk1)
                gr_k2, gc_k2 = self.get_location_in_goal_state(tk2)

                if flag1 != 0 and tk1 != 0 and gr_j1 == gr_k1 and tj1 != tk1 and ((j < k and gc_k1 < gc_j1)
                                                                  or (j > k and gc_k1 > gc_j1)):
                    c1[j].append(tk1)
                if flag2 != 0 and tk2 != 0 and gc_j2 == gc_k2 and tj2 != tk2 and ((j < k and gr_k2 < gr_j2)
                                                                  or (j > k and gr_k2 > gr_j2)):
                    c2[j].append(tk2)

        # Resolving conflicts in minimal number of moves
        conflict = 0
        while c1 != [[]]*n:
            num_max = len(c1[1])
            max_j = 1
            # Evaluate tile with maximum conflicts
            for j in range(n):
                if num_max < len(c1[j]):
                    num_max = len(c1[j])
                    max_j = j
            c1[max_j] = []
            conflict += 1
            # Removing conflict resolved tile
            for j in range(n):
                if len(c1[j]) > 0 and self.init_state[i][max_j] in c1[j]:
                    c1[j].remove(self.init_state[i][max_j])

        while c2 != [[]]*n:
            num_max = len(c2[1])
            max_j = 1
            # Evaluate tile with maximum conflicts
            for j in range(n):
                if num_max < len(c2[j]):
                    num_max = len(c2[j])
                    max_j = j
            c2[max_j]=[]
            conflict += 1
            # Removing conflict resolved tile
            for j in range(n):
                if len(c2[j]) > 0 and self.init_state[max_j][i] in c2[j]:
                    c2[j].remove(self.init_state[max_j][i])
        return conflict

    def get_location_in_goal_state(self, num):
        n = len(self.init_state)
        x_loc = (num - 1) / n
        y_loc = (num - 1) % n

        return x_loc, y_loc

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







