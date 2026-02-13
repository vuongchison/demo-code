#include <cassert>
#include <iostream>

#include "variable.hpp"
#include "constraint.hpp"
#include "solver.hpp"


void test_variables(){
    Variable var1({1, 2, 3});
    assert(var1.get_domain() == set<int>({1, 2, 3}));
    assert(!var1.is_assigned());
    
    var1.assign(1);
    assert(var1.is_assigned());
    assert(var1.get_value() == 1);
    
    var1.unassign();
    assert(!var1.is_assigned());
}

void test_constraints(){
    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({1}));
        NotEqualConstraint neq(var1, var2);
        assert(!neq.is_satisfied());
    }

    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1, 2}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({2, 3}));
        NotEqualConstraint neq(var1, var2);
        assert(neq.is_satisfied());
    }

    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1, 2}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({3, 4}));
        NotEqualConstraint neq(var1, var2);
        assert(neq.is_satisfied());
    }

    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1, 2}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({2, 3}));
        var1->assign(1);
        NotEqualConstraint neq(var1, var2);
        assert(neq.is_satisfied());
    }

    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1, 2}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({2, 3}));
        var1->assign(2);
        var2->assign(2);
        NotEqualConstraint neq(var1, var2);
        assert(!neq.is_satisfied());
    }

    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1, 2}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({2, 3}));
        var1->assign(2);
        var2->assign(3);
        NotEqualConstraint neq(var1, var2);
        assert(neq.is_satisfied());
    }
}

void test_solver(){
    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1, 2}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({2, 3}));
        shared_ptr<NotEqualConstraint> neq = make_shared<NotEqualConstraint>(var1, var2);
        CPSolver solver(vector<shared_ptr<Variable>>({var1, var2}), vector<shared_ptr<Constraint>>({neq}));
        const auto& solution = solver.solve();
        assert(solution.at(var1) != solution.at(var2));
    }

    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1, 2}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({2}));
        shared_ptr<NotEqualConstraint> neq = make_shared<NotEqualConstraint>(var1, var2);
        CPSolver solver(vector<shared_ptr<Variable>>({var1, var2}), vector<shared_ptr<Constraint>>({neq}));
        const auto& solution = solver.solve();
        assert(solution.at(var1) == 1);
        assert(solution.at(var2) == 2);
    }

    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1, 2}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({2, 3}));
        shared_ptr<Variable> var3 = make_shared<Variable>(set<int>({3, 4}));
        shared_ptr<Variable> var4 = make_shared<Variable>(set<int>({4}));
        shared_ptr<NotEqualConstraint> c1 = make_shared<NotEqualConstraint>(var1, var2);
        shared_ptr<NotEqualConstraint> c2 = make_shared<NotEqualConstraint>(var3, var2);
        shared_ptr<NotEqualConstraint> c3 = make_shared<NotEqualConstraint>(var4, var3);
        CPSolver solver(vector<shared_ptr<Variable>>({var1, var2, var3, var4}), vector<shared_ptr<Constraint>>({c1, c2, c3}));
        const auto& solution = solver.solve();
        assert(solution.at(var1) == 1);
        assert(solution.at(var2) == 2);
        assert(solution.at(var3) == 3);
        assert(solution.at(var4) == 4);
    }
}

void test_variable_propagate() {
    Variable v({1, 2, 3});
    v.add_to_domain(4);
    assert(v.get_domain() == set<int>({1, 2, 3, 4}));
    
    assert(v.remove_from_domain(3));
    assert(!v.remove_from_domain(3));
    assert(v.get_domain() == set<int>({1, 2, 4}));
}

void test_constraint_propagate() {
    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1, 2}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({2, 3}));
        NotEqualConstraint neq(var1, var2);
        var1->assign(2);
        neq.propagate(var1, 2);
        assert(var2->get_domain() == set<int>({3}));
    }

    {
        shared_ptr<Variable> var1 = make_shared<Variable>(set<int>({1, 2}));
        shared_ptr<Variable> var2 = make_shared<Variable>(set<int>({2, 3}));
        NotEqualConstraint neq(var1, var2);
        var1->assign(1);
        neq.propagate(var1, 1);
        assert(var2->get_domain() == set<int>({2, 3}));
    }
}

int main() {
    test_variables();
    test_constraints();
    test_solver();
    test_variable_propagate();
    test_constraint_propagate();
    cout << "All tests passed!" << endl;
    return 0; // All tests passed
}