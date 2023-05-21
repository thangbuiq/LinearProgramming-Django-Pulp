from django.contrib import admin
from .models import LinearProblem

admin.site.register(LinearProblem)
# Adds site header, site title, index title to the admin side.
admin.site.site_header = 'Linear Optimization Solver'
admin.site.site_title = 'HCMUS'
admin.site.index_title = 'Linear Optimization Solver'