from CP_solver import Variable, NotEqualConstraint, CPSolver

def test_variables():
    v1 = Variable({1, 2, 3})
    assert v1.domains == {1, 2, 3}
    assert not v1.is_assigned()
    assert v1.value is Variable.UNASSIGNED_FLAG

    v1.assign(1)
    assert v1.is_assigned()
    assert v1.value == 1

    v1.unassign()
    assert not v1.is_assigned()
    assert v1.value is Variable.UNASSIGNED_FLAG

def test_constraint():
    v1 = Variable({1})
    v2 = Variable({1})
    c = NotEqualConstraint(v1, v2)
    assert not c.is_satisfied()

    v1 = Variable({1, 2})
    v2 = Variable({2, 3})
    c = NotEqualConstraint(v1, v2)
    assert c.is_satisfied()

    v1 = Variable({1, 2})
    v2 = Variable({4, 3})
    c = NotEqualConstraint(v1, v2)
    assert c.is_satisfied()

    v1 = Variable({1, 2})
    v2 = Variable({2, 3})
    v1.assign(1)
    c = NotEqualConstraint(v1, v2)
    assert c.is_satisfied()

    v1 = Variable({1, 2})
    v2 = Variable({2, 3})
    v1.assign(2)
    v2.assign(2)
    c = NotEqualConstraint(v1, v2)
    assert not c.is_satisfied()

    v1 = Variable({1, 2})
    v2 = Variable({2, 3})
    v1.assign(2)
    v2.assign(3)
    c = NotEqualConstraint(v1, v2)
    assert c.is_satisfied()

def test_solver():
    v1 = Variable({1, 2})
    v2 = Variable({2, 3})
    c = NotEqualConstraint(v1, v2)
    solver = CPSolver({v1, v2}, {c})
    solution = solver.solve()
    assert solution[v1] != solution[v2]

    v1 = Variable({1, 2})
    v2 = Variable({2})
    c = NotEqualConstraint(v1, v2)
    solver = CPSolver({v1, v2}, {c})
    solution = solver.solve()
    assert solution[v1] == 1
    assert solution[v2] == 2


    v1 = Variable({1, 2})
    v2 = Variable({2, 3})
    v3 = Variable({3, 4})
    v4 = Variable({4})
    c1 = NotEqualConstraint(v1, v2)
    c2 = NotEqualConstraint(v3, v2)
    c3 = NotEqualConstraint(v3, v4)
    solver = CPSolver({v1, v2, v3, v4}, {c1, c2, c3})
    solution = solver.solve()
    assert solution[v1] == 1
    assert solution[v2] == 2
    assert solution[v3] == 3
    assert solution[v4] == 4