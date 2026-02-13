#include <vector>
#include <set>
#include <map>
#include <memory>
#include "constraint.hpp"
#include "variable.hpp"

class CPSolver {
private:
    vector<shared_ptr<Variable>> variables_;
    vector<shared_ptr<Constraint>> constraints_;
    map<shared_ptr<Variable>, int> solution_;
    map<shared_ptr<Variable>, vector<shared_ptr<Constraint>>> var_to_constraints_;

public:
    CPSolver(vector<shared_ptr<Variable>> vars, vector<shared_ptr<Constraint>> cons);
    ~CPSolver();

    const map<shared_ptr<Variable>, int>& solve();
private:
    bool backtrack();
    bool is_satisfied(shared_ptr<Variable> var = nullptr) const;
    shared_ptr<Variable> select_unassigned_variable() const;
    vector<pair<shared_ptr<Variable>, int>> propagate(shared_ptr<Variable> var, int val);
    void restore(vector<pair<shared_ptr<Variable>, int>> changes);
};