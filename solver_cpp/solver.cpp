#include "solver.hpp"
#include <iostream>

CPSolver::CPSolver(vector<shared_ptr<Variable>> variables, vector<shared_ptr<Constraint>> constraints) : variables_(variables), constraints_(constraints) {
    for (const shared_ptr<Constraint>& cons : constraints_) {
        for (const shared_ptr<Variable>& var : cons->get_variables()) {
            var_to_constraints_[var].push_back(cons);
        }
    }
};
CPSolver::~CPSolver(){
}

const map<shared_ptr<Variable>, int>& CPSolver::solve() {
    backtrack();
    return solution_;
}

bool CPSolver::backtrack() {
    shared_ptr<Variable> var = select_unassigned_variable();
    if (!var) {
        for (const shared_ptr<Variable>& var : variables_) {
            solution_[var] = var->get_value();
        }
        return true;
    }

    for (int val : var->get_domain()) {
        var->assign(val);
        if (is_satisfied(var)){
            if (backtrack()) {
                return true;
            }
        }
        var->unassign();
    }
    return false;
}

bool CPSolver::is_satisfied(shared_ptr<Variable> var) const {
    const vector<shared_ptr<Constraint>>& constraints = var ? var_to_constraints_.at(var) : constraints_;
    for (const shared_ptr<Constraint>& cons : constraints) {
        if (!cons->is_satisfied()) {
            return false;
        }
    }
    return true;
}

shared_ptr<Variable> CPSolver::select_unassigned_variable() const {
    for (const shared_ptr<Variable>& var : variables_) {
        if (!var->is_assigned()) {
            return var;
        }
    }
    return nullptr;
}

vector<pair<shared_ptr<Variable>, int>> CPSolver::propagate(shared_ptr<Variable> var, int val) {
    vector<pair<shared_ptr<Variable>, int>> changes;
    for(auto c: var_to_constraints_.at(var)) {
        auto change = c->propagate(var, val);
        if (change) {
            changes.push_back(*change);
        }
    
    return changes;
}
}

void CPSolver::restore(vector<pair<shared_ptr<Variable>, int>> changes) {
    for(auto [var, val] : changes) {
        var->add_to_domain(val);
    }
}
