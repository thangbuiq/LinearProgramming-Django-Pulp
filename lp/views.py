from django.shortcuts import render
from .models import LinearProblem

def lp_solve(request):
    if request.method == 'POST':
        objective = request.POST.get('objective')
        constraints = request.POST.get('constraints')
        sense = request.POST.get('sense')
        bounds = request.POST.get('bounds')

        lp_problem = LinearProblem(objective=objective, constraints_matrix=constraints, sense=sense, bounds=bounds)
        optimal_value, variable_values, lp_status = lp_problem.solve_problem()

        context = {
            'objective': objective,
            'constraints_matrix': constraints,
            'sense': sense,
            'bounds': bounds,
            'lp_status':lp_status,
            'optimal_value': optimal_value,
            'variable_values': variable_values,
        }
        return render(request, 'lp/result.html', context)

    return render(request, 'lp/form.html')
