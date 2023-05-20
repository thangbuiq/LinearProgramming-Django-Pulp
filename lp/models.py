from django.db import models
from pulp import LpProblem, LpVariable, LpMinimize, LpMaximize, lpSum, value

class LinearProblem(models.Model):
    objective = models.TextField()
    constraints_matrix = models.TextField()
    sense = models.CharField(max_length=10)

    def solve_problem(self):
        """
        Solve the linear programming problem and return the results.

        Returns:
            optimal_value (float): The optimal value of the objective function.
            variable_values (list): The values of the decision variables in the optimal solution.
        """
        objective = [float(val) for val in self.objective.split()]
        constraints = self.constraints_matrix.split('\n')
        constraints_matrix = [c.split() for c in constraints if c.strip()]
        sense = LpMinimize if self.sense == 'min' else LpMaximize

        n_variables = len(objective)
        n_constraints = len(constraints_matrix)

        lp_problem = LpProblem("Linear_Programming_Problem", sense)
        variables = [LpVariable(f"x_{i+1}", lowBound=0) for i in range(n_variables)]
        objective = lpSum(objective[i] * variables[i] for i in range(n_variables))
        lp_problem.setObjective(objective)

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
        optimal_value = value(lp_problem.objective)
        variable_values = [value(variables[i]) for i in range(n_variables)]

        return optimal_value, variable_values

    def display_result(self):
        """
        Solve the linear programming problem and display the results.
        """
        optimal_value, variable_values = self.solve_problem()
        print(">> Optimal Solution:")
        print(">> Optimal value:", optimal_value)
        print(">> Variable values:")
        for i, value in enumerate(variable_values, 1):
            print(f"x_{i}:", value)
