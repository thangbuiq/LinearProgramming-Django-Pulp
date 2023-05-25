from django.db import models
from pulp import LpProblem, LpVariable, LpMinimize, LpMaximize, lpSum, value, LpStatus
import tempfile
import os
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
            elif bound in ['free', 'f', 'freedom']:
                variables.append(LpVariable(f"x_{i+1}"))
            else:
                return None

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
            elif operator == "=" or operator == "==":
                lp_problem.addConstraint(constraint == rhs)
            else:
                return None

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
                optimal_value = "-∞"
            else:
                optimal_value = "+∞"
        elif (status == 'Infeasible'):
            lp_status ='-1'
            variable_values = None
            optimal_value = None
        # Write the LP problem to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
            lp_problem.writeLP(temp_file_path)
        
        # Read the contents of the temporary file
        with open(temp_file_path, 'r') as temp_file:
            output_str = temp_file.read()
        
        # Remove the temporary file
        os.remove(temp_file_path)
        return optimal_value, variable_values, lp_status, output_str.replace('\nEnd','').replace("\\* Linear_Programming_Problem *\\", "")

    def input_match(self):
        objective = [float(val) for val in self.objective.split()]
        constraints = self.constraints_matrix.split('\n')
        constraints_matrix = [c.split() for c in constraints if c.strip()]
        bounds = [str(val) for val in self.bounds.split()]
        n_variables = len(objective)
        n_constraints = len(constraints_matrix)
        """
        Check for numbers of the matching of variables.
        """
        if n_constraints == 0:
            return False
        if n_variables != len(bounds):
            return False
        for constraint in constraints_matrix:
            if (len(constraint) != n_variables + 2):
                return False
        # Return True by default
        return True
    def display_result(self): # Using only for testing in console
        """
        Solve the linear programming problem and display the results.
        """
        optimal_value, variable_values, lp_status = self.solve_problem()
        print(">> Optimal Solution:")
        print(">> Optimal value:", optimal_value)
        print(">> Variable values:")
        for i, value in enumerate(variable_values, 1):
            print(f"x_{i}:", value)
