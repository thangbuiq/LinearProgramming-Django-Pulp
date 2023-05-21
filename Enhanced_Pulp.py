from pulp import LpProblem, LpVariable, LpMinimize, LpMaximize, lpSum, value
import os
class LinearProblem:
    """
    Class representing a linear programming problem.
    Attributes:
        c: Coefficients of the objective function.
        A: Coefficients of the constraint matrix.
        b: Right-hand side values of the constraints.
        sense: The sense of optimization, either "min" (minimization) or "max" (maximization).
        n_variables: The number of decision variables.
        n_constraints: The number of constraints.
    Methods:
        __init__(self, c, A, b, sense): Initializes the linear programming problem.
        solve_problem(self): Solves the linear programming problem and return solved_problem.
        display_result(self): Solves problem and displays the results.
    """

    def __init__(self, c, A, b, sense):
        """
        Initialize the linear programming problem.

        Args:
            c (list): Coefficients of the objective function.
            A (list): Coefficients of the constraint matrix.
            b (list): Right-hand side values of the constraints.
            sense (str): The sense of optimization, either "min" or "max".
        """
        self.c = c
        self.A = A
        self.b = b
        self.sense = sense
        self.n_variables = len(c)
        self.n_constraints = len(A)

    def solve_problem(self):
        """
        Solve the linear programming problem and return the results.

        Returns:
            lp_problem (LpProblem): The linear programming problem.
            optimal_value (float): The optimal value of the objective function.
            variable_values (list): The values of the decision variables in the optimal solution.
        """
        lp_problem = LpProblem("Linear_Programming_Problem", self.sense)
        variables = [LpVariable(f"x_{i+1}", lowBound=0) for i in range(self.n_variables)]
        objective = lpSum(self.c[i] * variables[i] for i in range(self.n_variables))
        lp_problem.setObjective(objective)

        for i in range(self.n_constraints):
            constraint = lpSum(float(self.A[i][j]) * variables[j] for j in range(self.n_variables))
            operator = self.A[i][-2]
            rhs = float(self.A[i][-1])
            if operator == "<=":
                lp_problem.addConstraint(constraint <= rhs)
            elif operator == ">=":
                lp_problem.addConstraint(constraint >= rhs)
            else:
                lp_problem.addConstraint(constraint == rhs)

        lp_problem.solve()
        optimal_value = value(lp_problem.objective)
        variable_values = [value(variables[i]) for i in range(self.n_variables)]

        return lp_problem, optimal_value, variable_values

    def display_result(self):
        """
        Solve the linear programming problem and display the results.
        """
        problem, optimal_value, variable_values = self.solve_problem()
        print(problem, end="\n\n")
        print(">> Optimal Solution:")
        print(">> Optimal value:", optimal_value)
        print(">> Variable values:")
        for i, value in enumerate(variable_values, 1):
            print(f"x_{i}:", value)
