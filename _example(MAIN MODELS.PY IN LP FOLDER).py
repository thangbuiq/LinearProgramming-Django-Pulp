from ipaddress import v4_int_to_packed
from pulp import LpProblem, LpVariable, LpMinimize, LpMaximize, lpSum, value, LpStatus
import numpy as np
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

    def __init__(self, c, A, bounds, sense):
        """
        Initialize the linear programming problem.

        Args:
            c (list): Coefficients of the objective function.
            A (list): Coefficients of the constraint matrix.
            bounds (list): Right-hand side values of the constraints.
            sense (str): The sense of optimization, either "min" or "max".
        """
        self.c = c
        self.A = A
        self.bounds = bounds
        self.sense = sense
        self.n_variables = len(c)
        self.n_constraints = len(A)
        self.status = None 

    def solve_problem(self):
        """
        Solve the linear programming problem and return the results.

        Returns:
            lp_problem (LpProblem): The linear programming problem.
            optimal_value (float): The optimal value of the objective function.
            variable_values (list): The values of the decision variables in the optimal solution.
        """
        lp_problem = LpProblem("Linear_Programming_Problem", self.sense)
        variables = []
        for i in range(len(self.bounds)):
            bound = self.bounds[i]
            if bound == '>=':
                variables.append(LpVariable(f"x_{i+1}", lowBound=0))
            elif bound == '<=':
                variables.append(LpVariable(f"x_{i+1}", upBound=0))
            else:
                variables.append(LpVariable(f"x_{i+1}"))
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
        status = LpStatus[lp_problem.status]
        lp_status = None
        if (status == 'Optimal'):
            lp_status = '1'
            optimal_value = value(lp_problem.objective)
            vars_not_0 = [x for x in self.c if x != 0]
            if (len(vars_not_0) < self.n_constraints):
                variable_values = []
                for i in range(self.n_variables):
                    if (self.c[i]==0):
                        variable_values.append(f'{value(variables[i])} + w{i}')
                    else:
                        variable_values.append(value(variables[i]))
            else:
                variable_values = [value(variables[i]) for i in range(self.n_variables)]
        elif (status == 'Unbounded'):
            lp_status = '-2'
            variable_values= None
            if (self.sense == LpMinimize):
                optimal_value = -np.inf
            else:
                optimal_value = np.inf
        elif (status == 'Infeasible'):
            lp_status ='-1'
            variable_values = None
            optimal_value = None

        return lp_problem, optimal_value, variable_values, lp_status

    def display_result(self):
        """
        Solve the linear programming problem and display the results.
        """
        problem, optimal_value, variable_values, status = self.solve_problem()
        print(problem, end="\n\n")
        if status == '1':
            print(">> Status Solution: Bai toan toi uu")
        elif status == '-1':
            print(">> Status Solution: Bai toan vo nghiem")
        else:
            print(">> Status Solution: Bai toan khong gioi noi")
        print(">> Optimal value: ", optimal_value)
        print(">> Variable values:")
        if status == '1':
            for i, value in enumerate(variable_values, 1):
                print(f"x_{i}:", value)
        elif status == '-1':
            print(variable_values)
        else:
            print(variable_values)
