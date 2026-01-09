from CP_solver import Variable, NotEqualConstraint, CPSolver

_ = None
sudoku = [[_, _, 4, 6, _, _, _, _, _],
          [_, 3, 9, 1, 2, _, 6, _, _],
          [_, _, _, 4, 9, _, _, _, _],

          [7, _, _, _, _, _, _, _, 5],
          [_, _, 3, 9, _, 6, _, _, _],
          [4, _, _, _, _, 1, 9, _, _],
          
          [_, _, _, _, _, _, _, 5, _],
          [1, _, _, 7, _, _, _, _, 3],
          [_, _, _, 5, 3, _, _, _, 8]]

variables = list()

for i in range(9):
    for j in range(9):
        if sudoku[i][j] == _:
            variable = Variable(set(range(1, 10)))
            variables.append(variable)
            sudoku[i][j] = variable
        else:
            variable = Variable({sudoku[i][j]})
            variable.assign(sudoku[i][j])
            variables.append(variable)
            sudoku[i][j] = variable

constraints = list()
for c1 in range(9):
    for c2 in range(9):
        for r1 in range(9):
            for r2 in range(9):
                if r1 * 9 + c1 >= r2 * 9 + c2:
                    continue
                if (c1 == c2) or (r1 == r2) or ((c1 // 3 == c2 // 3) and (r1 // 3 == r2 // 3)):
                    c = NotEqualConstraint(sudoku[r1][c1], sudoku[r2][c2])
                    constraints.append(c)

solver = CPSolver(variables, constraints)
solution = solver.solve()

for i in range(9):
    for j in range(9):
        print(solution.get(sudoku[i][j], "?"), end=" ")
    print()