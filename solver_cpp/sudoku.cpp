#include <memory>
#include <iostream>

#include "solver.hpp"


int _ = 0;
vector<vector<int>> sudoku_board = {
    {_, _, 4,  6, _, _,  _, _, _},
    {_, 3, 9,  1, 2, _,  6, _, _},
    {_, _, _,  4, 9, _,  _, _, _},

    {7, _, _,  _, _, _,  _, _, 5},
    {_, _, 3,  9, _, 6,  _, _, _},
    {4, _, _,  _, _, 1,  9, _, _},
    
    {_, _, _,  _, _, _,  _, 5, _},
    {1, _, _,  7, _, _,  _, _, 3},
    {_, _, _,  5, 3, _,  _, _, 8}
};


int main(){
    vector<shared_ptr<Variable>> variables;
    vector<shared_ptr<Constraint>> constraints;
    shared_ptr<Variable> grid[9][9];

    for(int i = 0; i < 9; i++) {
        for(int j = 0; j < 9; j++) {
            if(sudoku_board[i][j] == _){
                variables.push_back(make_shared<Variable>(set<int>{1,2,3,4,5,6,7,8,9}));
            } else {
                variables.push_back(make_shared<Variable>(set<int>{sudoku_board[i][j]}));
            }
            grid[i][j] = variables.back();
        }
    }
    for(int c1 = 0; c1 < 9; c1++) {
        for(int r1 = 0; r1 < 9; r1++) {
            for(int c2 = 0; c2 < 9; c2++) {
                for(int r2 = 0; r2 < 9; r2++) {
                    if (r1 * 9 + c1 >= r2 * 9 + c2) {
                        continue;
                    }
                    if((c1 == c2) || (r1 == r2) || (c1/3 == c2/3 && r1/3 == r2/3)) {
                        constraints.push_back(make_shared<NotEqualConstraint>(grid[r1][c1], grid[r2][c2]));
                    }
                }
            }
        }
    }
    CPSolver solver(variables, constraints);
    const auto& solution = solver.solve();

    for(int i = 0; i < 9; i++) {
        for(int j = 0; j < 9; j++) {
            cout << solution.at(grid[i][j]) << " ";
        }
        cout << endl;
    }

}