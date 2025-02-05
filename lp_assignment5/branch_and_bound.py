from ortools.linear_solver import pywraplp


def LinearProgrammingExample():
    """Linear programming sample."""
    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return

    # Create the two variables and let them take on any non-negative value.
    x1 = solver.NumVar(0, solver.infinity(), "x1")
    x2 = solver.NumVar(0, solver.infinity(), "x2")

    print("Number of variables =", solver.NumVariables())

    # Constraint 0: x + 2y <= 14.
    solver.Add(4 * x1 + 9 * x2 <= 26.0)

    # Constraint 1: 3x - y >= 0.
    solver.Add(8 * x1 + 5 * x2 <= 17.0)

    # solver.Add(x2 == 2.0)

    # solver.Add(x2 <= 2.0)

    # solver.Add(x1 >= 1.0)

    # solver.Add(x2 <= 1.0)

    solver.Add(x1 >= 2.0)

    solver.Add(x2 <= 0.0)

    solver.Add(x1 >= 3.0)


    print("Number of constraints =", solver.NumConstraints())

    # Objective function: 3x + 4y.
    solver.Maximize(4 * x1 + 3 * x2)

    # Solve the system.
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print(f"z = {solver.Objective().Value():0.1f}")
        print(f"x1 = {x1.solution_value():0.2f}")
        print(f"x2 = {x2.solution_value():0.2f}")
    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")


def IP():
    # Create the mip solver with the CP-SAT backend.
    # solver = pywraplp.Solver.CreateSolver("SAT")
    solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING) 
    if not solver:
        return

    infinity = solver.infinity()
    # x and y are integer non-negative variables.
    x1 = solver.IntVar(0.0, infinity, "x1")
    x2 = solver.IntVar(0.0, infinity, "x2")

    print("Number of variables =", solver.NumVariables())

    # Constraint 0: x + 2y <= 14.
    solver.Add(4 * x1 + 9 * x2 <= 26.0)

    # Constraint 1: 3x - y >= 0.
    solver.Add(8 * x1 + 5 * x2 <= 17.0)

    print("Number of constraints =", solver.NumConstraints())

    # Maximize x + 10 * y.
    solver.Maximize(4 * x1 + 3 * x2)

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    print("hi")

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("z =", solver.Objective().Value())
        print("x1 =", x1.solution_value())
        print("x2 =", x2.solution_value())
    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")

# LinearProgrammingExample()
IP()