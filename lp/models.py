from django.db import models
from pulp import LpProblem, LpVariable, LpMinimize, LpMaximize, lpSum, value, LpStatus
import numpy as np
class LinearProblem(models.Model):
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
        solve_problem(self): Solves the linear programming problem and return solved_problem.
        display_result(self): Solves problem and displays the results.
    """
    objective = models.TextField()
    constraints_matrix = models.TextField()
    sense = models.CharField(max_length=10)
    bounds = models.TextField()
    def solve_problem(self):
        """
        Solve the linear programming problem and return the results.

        Returns:
            lp_problem (LpProblem): The linear programming problem.
            optimal_value (float): The optimal value of the objective function.
            variable_values (list): The values of the decision variables in the optimal solution.
        """
        objective = [float(val) for val in self.objective.split()]
        constraints = self.constraints_matrix.split('\n')
        constraints_matrix = [c.split() for c in constraints if c.strip()]
        sense = LpMinimize if self.sense == 'min' else LpMaximize
        bounds = [str(val) for val in self.bounds.split()]
        n_variables = len(objective)
        n_constraints = len(constraints_matrix)


        lp_problem = LpProblem("Linear_Programming_Problem", sense)
        """
        variables = [LpVariable(f"x_{i+1}", lowBound=0) for i in range(n_variables)]
        objective = lpSum(objective[i] * variables[i] for i in range(n_variables))
        """
        variables = []
        for i in range(len(bounds)):
            bound = bounds[i]
            if bound == '>=':
                variables.append(LpVariable(f"x_{i+1}", lowBound=0))
            elif bound == '<=':
                variables.append(LpVariable(f"x_{i+1}", upBound=0))
            else:
                variables.append(LpVariable(f"x_{i+1}"))
        objective_ = lpSum(objective[i] * variables[i] for i in range(n_variables))
        lp_problem.setObjective(objective_)

        for i in range(n_constraints):
            constraint = lpSum(float(constraints_matrix[i][j]) * variables[j] for j in range(n_variables))
            operator = constraints_matrix[i][-2]
            rhs = float(constraints_matrix[i][-1])
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
            vars_not_0 = [x for x in objective if x != 0]
            if (len(vars_not_0) < n_constraints):
                variable_values = []
                for i in range(n_variables):
                    if (objective[i]==0):
                        variable_values.append(f'{value(variables[i])} + w{i}')
                    else:
                        variable_values.append(value(variables[i]))
            else:
                variable_values = [value(variables[i]) for i in range(n_variables)]
        elif (status == 'Unbounded'):
            lp_status = '-2'
            variable_values= None
            if (sense == LpMinimize):
                optimal_value = -np.inf
            else:
                optimal_value = np.inf
        elif (status == 'Infeasible'):
            lp_status ='-1'
            variable_values = None
            optimal_value = None

        return optimal_value, variable_values, lp_status

    def display_result(self):
        """
        Solve the linear programming problem and display the results.
        """
        optimal_value, variable_values, lp_status = self.solve_problem()
        print(">> Optimal Solution:")
        print(">> Optimal value:", optimal_value)
        print(">> Variable values:")
        for i, value in enumerate(variable_values, 1):
            print(f"x_{i}:", value)
