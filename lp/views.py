from django.shortcuts import render
from django.contrib import messages
from .models import LinearProblem

def lp_solve(request):
    
    if request.method == 'POST':
        objective = request.POST.get('objective')
        constraints = request.POST.get('constraints')
        sense = request.POST.get('sense')
        bounds = request.POST.get('bounds')
        lp_problem = LinearProblem(objective=objective, constraints_matrix=constraints, sense=sense, bounds=bounds)
        # Check if input_match() returns False
        if not lp_problem.input_match():
            messages.warning(request, 'Invalid input. Please check your constraints.')
            return render(request, 'lp/form.html')
        optimal_value, variable_values, lp_status, prob_str = lp_problem.solve_problem()
        if lp_status == '1':
            status = "Tối ưu"
        elif lp_status == '-1':
            status = "Vô nghiệm"
        else:
            status = "Không giới nội"
        context = {
            'objective': objective,
            'constraints_matrix': constraints,
            'sense': sense,
            'bounds': bounds,
            'lp_status': status,
            'optimal_value': optimal_value,
            'variable_values': variable_values,
            'prob_str':prob_str,
        }
        # Add the 'result' context variable to be used in form.html
        context['result'] = True
        return render(request, 'lp/form.html', context)

    return render(request, 'lp/form.html')