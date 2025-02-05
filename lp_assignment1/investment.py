#!/user/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver('investment', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Create the two variables and let them take on any value.
    total = 1000000
    x2 = solver.NumVar(0.0, 1000000, 'x2')
    x3 = solver.NumVar(0.0, 1000000, 'x3')
    x4 = solver.NumVar(0.0, 1000000, 'x4')

    # Constraint 2
    constraint2 = solver.Constraint(0, solver.infinity())
    constraint2.SetCoefficient(x2, 2)
    constraint2.SetCoefficient(x3, -1)
    constraint2.SetCoefficient(x4, -3)

    # Constraint 3
    threshold = total * 0.4
    constraint31 = solver.Constraint(-solver.infinity(), threshold)
    constraint31.SetCoefficient(x2, 1)

    constraint32 = solver.Constraint(-solver.infinity(), threshold)
    constraint32.SetCoefficient(x3, 1)

    constraint33 = solver.Constraint(-solver.infinity(), threshold)
    constraint33.SetCoefficient(x4, 1)

    # constraint31 = solver.Constraint(-solver.infinity(), 0)
    # constraint31.SetCoefficient(x2, 0.6)
    # constraint31.SetCoefficient(x3, -0.4)
    # constraint31.SetCoefficient(x4, -0.4)

    # constraint32 = solver.Constraint(-solver.infinity(), 0)
    # constraint32.SetCoefficient(x2, -0.4)
    # constraint32.SetCoefficient(x3, 0.6)
    # constraint32.SetCoefficient(x4, -0.4)

    # constraint33 = solver.Constraint(-solver.infinity(), 0)
    # constraint33.SetCoefficient(x2, -0.4)
    # constraint33.SetCoefficient(x3, -0.4)
    # constraint33.SetCoefficient(x4, 0.6)

    # Constraint 4
    constraint4 = solver.Constraint(-solver.infinity(), 1000000)
    constraint4.SetCoefficient(x2, 1)
    constraint4.SetCoefficient(x3, 1)
    constraint4.SetCoefficient(x4, 1)

    # Objective function:
    objective = solver.Objective()
    objective.SetCoefficient(x2, 0.08 / 4)
    objective.SetCoefficient(x3, 0.12 / 7)
    objective.SetCoefficient(x4, 0.14 / 9)
    objective.SetMaximization()

    # Solve the system.
    solver.Solve()
    opt_solution = 0.08 / 4 * x2.solution_value() + 0.12 / 7 * x3.solution_value() + 0.14 / 9 * x4.solution_value()
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())
    # The value of each variable in the solution.
    print('Solution:')
    print('x2 = ', x2.solution_value())
    print('x3 = ', x3.solution_value())
    print('x4 = ', x4.solution_value())
    # The objective value of the solution.
    print('Optimal objective value =', opt_solution)

LinearProgrammingExample()