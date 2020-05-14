import os
import sys
import time
from 8-puzzle-IDS import Puzzle as Puz1
from Astar-manhattan import Puzzle as Puz2
from Astar-euclidean import Puzzle as Puz3
from Astar-euclidean import Puzzle as Puz4

if __name__ == "__main__":
    """
    
    How to replicate experiments?
    
    
    This file takes any puzzle as input and produces stats for that file
    One can run this script again for other inputs also.
    
    TO RUN: python2 CS3243_P1_26_5.py public_tests_p1/n_equals_3/input_2.txt output.txt
    NOTE: We do this so that we can get stats for each puzzle one by one rather than let it run for a long time
    
    Result format:
    ```
     Heuristic 2(Linear Conflicts) Nodes Explored: [0, 2, 4, 5, 7, 11, 27, 30, 35, 64, 114, 148, 150, 152, 154, 227, 329, 373, 534, 688, 691, 694, 697]
     Size of Priority Queue: 1, 3, 16, 37, 110, 193, 491, 624, 658, 696, 692, 695, 693, 687, 690, 680, 667, 682, 685, 456, 457, 458, 460
     Total Nodes: [1, 5, 20, 42, 117, 204, 518, 654, 693, 760, 806, 843, 843, 839, 844, 907, 996, 1055, 1219, 1144, 1148, 1152, 1157]
     Number of steps: 22
     Initial H cost: 12
     Time taken (s): 0.168179988861
     Average heuristic cost: 7.86363636364
    ```
    
    === For our experiment 1, we ran with following inputs ===
    Its to compare hoe heuristics scale in num of nodes explored with difficulty of puzzle

    # Size 5 and Level moderate
    init_state =   [[1 3 4 0 10],
                    [7 2 12 8 5],
                    [6 11 13 15 14],
                    [17 23 18 9 19],
                    [16 21 22 24 20]]
                    
    # Size 3 and Level moderate
    init_state =   [[1 8 3],
                    [5 2 4],
                    [0 7 6]]
                    
    # Size 4 and Level difficult
    init_state =      [[13 5 3 4],
                        [2 1 8 0],
                        [9 15 10 11],
                        [14 12 6 7]]
         
                        
    # Size 5 and Level Easy
    init_state =       [[1 2 3 4 5],
                        [6 7 8 9 10],
                        [11 12 0 14 15],
                        [16 17 13 20 19],
                        [21 22 23 18 24]]
    
    === For experiment 2 we run inputs with size 3 and compare IDS with A* search ===
    
    """

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

    analysis = 'Cost Analysis\n\n'

    if n == 3:
        puzzle_heur0 = Puz1(init_state, goal_state, set())
        init_time = time.time()
        ans = puzzle_heur0.solve()
        total_time = time.time() - init_time

        analysis += 'Iterative Deepening Search Nodes Explored: ' + str(puzzle_heur0.explored) + '\n Search Size at Depths:'
        analysis += ' ' + (str(puzzle_heur0.num_nodes)[1:-1])
        analysis += '\n Number of steps: ' + str(len(ans)) + '\n'
        analysis += ' Time taken (s): ' + str(total_time) + '\n'
        analysis = analysis + '\n'

    puzzle_heur1 = Puz2(init_state, goal_state)
    init_time = time.time()
    ans, average_h_cost = puzzle_heur1.solve()
    total_time = time.time() - init_time
    explored_total = [puzzle_heur1.explored[i] + puzzle_heur1.num_nodes[i] for i in range(len(puzzle_heur1.explored))]

    analysis += 'Heuristic 1(Manhattan) Nodes Explored: ' + str(puzzle_heur1.explored) + '\n'
    analysis += ' Size of Priority Queue: ' + (str(puzzle_heur1.num_nodes)[1:-1])
    analysis += '\n Total Nodes: ' + str(explored_total)
    analysis += '\n Number of steps: ' + str(len(ans)) + '\n'
    analysis += ' Initial H cost: ' + str(puzzle_heur1.h_cost()) + '\n'
    analysis += ' Time taken (s): ' + str(total_time) + '\n'
    analysis += ' Average heuristic cost: ' + str(average_h_cost) + '\n'
    analysis = analysis + '\n'

    puzzle_heur2 = Puz3(init_state, goal_state)
    init_time = time.time()
    ans, average_h_cost = puzzle_heur2.solve()
    total_time = time.time() - init_time
    explored_total = [puzzle_heur2.explored[i] + puzzle_heur2.num_nodes[i] for i in range(len(puzzle_heur2.explored))]

    analysis += 'Heuristic 2(Linear Conflicts) Nodes Explored: ' + str(puzzle_heur2.explored) + '\n'
    analysis += ' Size of Priority Queue: ' + (str(puzzle_heur2.num_nodes)[1:-1])
    analysis += '\n Total Nodes: ' + str(explored_total)
    analysis += '\n Number of steps: ' + str(len(ans)) + '\n'
    analysis += ' Initial H cost: ' + str(puzzle_heur2.h_cost()) + '\n'
    analysis += ' Time taken (s): ' + str(total_time) + '\n'
    analysis += ' Average heuristic cost: ' + str(average_h_cost) + '\n'
    analysis = analysis + '\n'

    puzzle_heur3 = Puz4(init_state, goal_state)
    init_time = time.time()
    ans, average_h_cost = puzzle_heur3.solve()
    total_time = time.time() - init_time
    explored_total = [puzzle_heur3.explored[i] + puzzle_heur3.num_nodes[i] for i in range(len(puzzle_heur3.explored))]

    analysis += 'Heuristic 3(Euclidean) Nodes Explored: ' + str(puzzle_heur3.explored) + '\n'
    analysis += ' Size of Priority Queue: ' + (str(puzzle_heur3.num_nodes)[1:-1])
    analysis += '\n Total Nodes: ' + str(explored_total)
    analysis += '\n Number of steps: ' + str(len(ans)) + '\n'
    analysis += ' Initial H cost: ' + str(puzzle_heur3.h_cost()) + '\n'
    analysis += ' Time taken (s): ' + str(total_time) + '\n'
    analysis += ' Average heuristic cost: ' + str(average_h_cost) + '\n'
    analysis = analysis + '\n'

    with open(sys.argv[2], 'a') as f:
        # for answer in ans:
        #     f.write(answer + '\n')
        f.write(analysis)






