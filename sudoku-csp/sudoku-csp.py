import sys
from Queue import PriorityQueue
import math

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.n = len(self.puzzle)
        self.ans = self.copy(puzzle)  # self.ans is a list of lists
        self.constrainList = self.constraints()
        self.backtrackNum = 0
        self.variable_heuristics = "MRV"  # Possible values "MRV" "MCV"
        self.value_heuristics = "NONE"  # Possible values "LCV", "NONE"
        self.checks_heuristics = "MAC"  # Possible values "MAC" "FC"

    def copy(self, puz):
        return [[x for x in row] for row in puz]

    def getIndex(self, i, j):
        """
        Global indexing to covert (i,j) to int
        :param i: x
        :param j: y
        :return: int (single val for (x, y)
        """
        return i * self.n + j

    def getRowCol(self, index):
        return [index/self.n, index - (index/self.n)*self.n]

    def neighbours(self, index):
        """
        Checks row, column and box neighbours with possible conflicts for a cell
        :param index:
        :return:
        """
        c = []
        [i, j] = self.getRowCol(index)
        for k in range(self.n):

            # Adding row neighbour
            c_ = self.getIndex(i, k)
            if c_ not in c:
                c.append(c_)

            # Adding column neighbour
            c_ = self.getIndex(k, j)
            if c_ not in c:
                c.append(c_)

            # Adding square neighbour
            boxStartR = int(i / math.sqrt(self.n)) * int(math.sqrt(self.n))
            boxR = boxStartR + k / 3
            boxStartC = int(j / math.sqrt(self.n)) * int(math.sqrt(self.n))
            boxC = boxStartC + k % 3

            c_ = self.getIndex(boxR, boxC)
            if c_ not in c:
                c.append(c_)

        c.remove(self.getIndex(i, j))
        return c

    def constraint(self, i, j):
        """
        Gets constraint for a given (i, j) cell
        :return: Array of array [referenced through indexes]
        """
        c = []
        for k in range(self.n):

            # Adding row constraint
            c_ = [self.getIndex(i, j), self.getIndex(i, k)]
            if c_ not in c:
                c.append(c_)

            # Adding column constraints
            c_ = [self.getIndex(i, j), self.getIndex(k, j)]
            if c_ not in c:
                c.append(c_)

            # Adding square constraints
            boxStartR = int(i / math.sqrt(self.n)) * int(math.sqrt(self.n))
            boxR = boxStartR + k / 3
            boxStartC = int(j / math.sqrt(self.n)) * int(math.sqrt(self.n))
            boxC = boxStartC + k % 3

            c_ = [self.getIndex(i, j), self.getIndex(boxR, boxC)]
            if c_ not in c:
                c.append(c_)

        c.remove([self.getIndex(i, j), self.getIndex(i, j)])
        return c

    def constraints(self):
        """
        Return all set of constraints
        """
        c = []
        for i in range(self.n):
            for j in range(self.n):
                c.append(self.constraint(i, j))
        return c

    def MRV(self, domain, assigned):
        """
        Minimum Remaining Values Heuristic for Variable selection 
        :param domain: domain array
        :param assigned: assigned variabled
        :return: index (x, y)
        """
        len_domain = len(domain)
        min_len = 10
        idx = 1
        for j in range(len_domain):
            len_j = len(domain[j])
            if not assigned[j] and len_j < min_len:
                min_len = len_j
                idx = j

        return idx

    def MCV(self, assigned):
        """
        Degree Heuristic for variable selection
        :param assigned: Assigned variables
        :return: index (x, y)
        """
        pq = PriorityQueue()

        # assign row and col conflict scores, and assign values to tileDomain
        for row in range(self.n):
            for col in range(self.n):
                if not assigned[self.getIndex(row, col)]:
                    neighbours = self.neighbours(self.getIndex(row, col))
                    x = 0
                    for n in neighbours:
                        if not assigned[n]:
                            x += 1
                    pq.put((x, self.getIndex(row, col)))

        [val, idx] = pq.get()
        return idx

    def LCV(self, domain, index):
        """
        LCV for Value choosing heuristic
        :param domain: domain of values
        :param index: index of domain for which values are chosen
        :return: 
        """
        if len(domain[index]) == 1:
            return domain[index]

        return self.get_order_by_conflicts(domain, index)

    def get_unassigned_variable(self, domain, assigned):
        if self.variable_heuristics == "MRV":
            return self.MRV(domain, assigned)
        elif self.variable_heuristics == "MCV":
            return self.MCV(assigned)

    def order_domain_values(self, domain, cell):
        if self.value_heuristics == "LCV":
            return self.LCV(domain, cell)
        else:
            return domain[cell]

    def is_consistent(self, domain, assigned, cell, value):
        """
        Checks if the assignment is consistent
        """
        is_consistent = True

        # Redundant assignment will be consistent by virtue of forward checks
        [i, j] = self.getRowCol(cell)
        constraints = self.constrainList[self.getIndex(i, j)]

        for c in constraints:
            [i_,j_] = self.getRowCol(c[1])
            if assigned[c[1]] and domain[c[1]] == [value]:
                is_consistent = False

        return is_consistent

    def assign(self, domain, assigned, cell, value):
        domain2 = self.copy(domain)
        assigned2 = [x for x in assigned]
        ok = True

        if self.checks_heuristics == "FC":
            domain2 = self.forward_check(domain2, assigned, cell, value)
        elif self.checks_heuristics == "MAC":
            [ok, domain2] = self.MAC(domain2, assigned2, cell, value)

        return [ok, domain2, assigned2]

    def forward_check(self, domain, assigned, cell, value):

        domain[cell] = [value]
        constraints = self.constrainList[cell]
        for c in constraints:
            if not assigned[c[1]]:
                if len(domain[c[1]]) is not 0 and value in domain[c[1]]:
                    domain[c[1]].remove(value)
        return domain

    def MAC(self, domain, assigned, cell, value):
        """
        Reduces domain set of the variables through Arc Consistency
        """
        check_queue = [cell]
        domain[cell] = [value]
        while len(check_queue) is not 0:
            t = check_queue.pop()
            constraints = self.constrainList[t]
            for c in constraints:
                if domain[t][0] in domain[c[1]]:
                    domain[c[1]].remove(domain[t][0])
                    if len(domain[c[1]]) == 0:
                        return [False, domain]
                    if c[1] not in check_queue and len(domain[c[1]]) == 1:
                        check_queue.append(c[1])

        ok = True
        len_domain = len(domain)
        for j in range(len_domain):
            if not assigned[j] and len(domain[j]) == 1:
                if self.is_consistent(domain, assigned, j, domain[j][0]):
                    assigned[j] = True
                else:
                    ok = False
        return [ok, domain]

    def get_order_by_conflicts(self, domain, index):
        counter = dict((k, 0) for k in domain[index])
        for n in self.neighbours(index):
            for val in domain[index]:
                if len(domain[n]) > 1 and val in domain[n]:
                    counter[val] += 1

        return [tup[0] for tup in sorted(counter.items(), key=lambda kv: (kv[1], kv[0]))]

    def backtrack(self, domain, assigned):
        """
        Recursively backtracks to find solution
        :param domain:
        :param assigned:
        :return:
        """

        if assigned == [True] * 81:
            return domain

        cell = self.get_unassigned_variable(domain, assigned)  # select-unassigned-variables(csp)

        for value in self.order_domain_values(domain, cell):  # order-domain-values(csp, var) No recursion if domain empty

            # if value is consistent with assignment then assign the variable
            assigned[cell] = True
            [ok, domain_trim, assigned_2] = self.assign(domain, assigned, cell, value)

            if not ok:
                continue

            result = self.backtrack(domain_trim, assigned_2)
            self.backtrackNum = self.backtrackNum + 1

            # If result is True then end backtracking
            if result:
                return result

            # remove {cell = value} from assignment
            assigned[cell] = False

        # Failure
        return False

    def solve(self):

        # list of domains for all variables
        domain = [[1, 2, 3, 4, 5, 6, 7, 8, 9] for i in range(self.n*self.n)]

        # which values have been assigned
        assigned = [False for i in range(self.n*self.n)]

        # Assigning the domains to the CSP based on the currently known puzzle after running a preprocess forward check
        for i in range(self.n):
            for j in range(self.n):
                if self.puzzle[i][j] != 0:
                    assigned[self.getIndex(i, j)] = True
                    domain = self.forward_check(domain, assigned, self.getIndex(i, j), self.puzzle[i][j])

        # [Result,domain] = self.AC3_preprocess(domain,assigned)
        self.ans = self.backtrack(domain, assigned)

        for j in range(self.n*self.n):
            [a, b] = self.getRowCol(j)
            self.puzzle[a][b] = self.ans[j].pop()

        # for experimental testing    
        # print self.backtrackNum, "backtracks"

        return self.puzzle

    # ================ UNUSED FUNCTIONS ======================

    def AC3_preprocess(self, domain, assigned):
        queue = []
        for c in self.constrainList:
            queue.extend(c)

        while len(queue) != 0:
            [i1, i2] = queue.pop()
            if self.alldiff(domain, i1, i2):
                if len(domain[i1]) == 0:
                    return [False,domain]
                for a in self.neighbours(self.getIndex(i, j)):
                    if a != i2 and [a, i1] not in queue:
                        queue.append([a, i1])

        return [True, domain]

    def alldiff(self, domain, idx1, idx2):
        """
        Check if given sudoku location's domain set is alldiff arc consistent with the tiles
        :return: Boolean
        """
        revised = False

        if domain[idx2][0] in domain[idx1]:
            domain[idx1].remove(domain[idx2][0])
            revised = True

        return revised

    def conflicts(self, domain, index, val):
        count = 0
        for n in self.neighbours(index):
            if len(domain[n]) > 1 and val in domain[n]:
                count += 1

        return count


if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
