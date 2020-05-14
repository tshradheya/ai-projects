# Sudoku using CSP

## Heuristics Implemented

- Inference:
  - Maintaining Arc Consistency(AC3)
  - Forward Checking
- Variable:
  - Miniumum Remaining Values
  - Degree
- Value
  - Least Constraining Value

[Technical Report](https://github.com/tshradheya/ai-projects/blob/master/sudoku-csp/Report.pdf)


## Usage

`python2 sudoku-csp.py public_tests_p2_sudoku/input1.txt public_tests_p2_sudoku/sol1.txt`