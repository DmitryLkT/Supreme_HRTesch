from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count, Max, Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from .models import Module, ModuleCompletion
from .permissions import hr_required


def employees_queryset():
    return get_user_model().objects.filter(
        is_active=True, is_superuser=False, is_staff=False,
    ).exclude(groups__name="HR")


@hr_required
@require_GET
def hr_dashboard(request):
    total_modules = Module.objects.filter(is_published=True).count()
    published = Q(modulecompletion__module__is_published=True)
    employees = employees_queryset().annotate(
        completed_count=Count("modulecompletion__module_id", filter=published, distinct=True),
        last_completed_at=Max("modulecompletion__completed_at", filter=published),
    )
    employee_count = employees.count()
    finished_count = employees.filter(completed_count=total_modules).count() if total_modules else 0
    in_progress_count = employees.filter(
        completed_count__gt=0, completed_count__lt=total_modules,
    ).count()

    query = request.GET.get("q", "").strip()[:100]
    if query:
        for word in query.split():
            employees = employees.filter(
                Q(username__icontains=word) | Q(first_name__icontains=word)
                | Q(last_name__icontains=word)
            )
    page = Paginator(employees.order_by("last_name", "first_name", "username", "id"), 20).get_page(request.GET.get("page"))
    for employee in page.object_list:
        employee.progress_percent = round(employee.completed_count / total_modules * 100) if total_modules else 0

    return render(request, "onboarding/hr_dashboard.html", {
        "page_obj": page, "query": query,
        "total_modules": total_modules,
        "employee_count": employee_count,
        "finished_count": finished_count,
        "in_progress_count": in_progress_count,
        "not_started_count": employee_count - finished_count - in_progress_count,
    })


@hr_required
@require_GET
def hr_employee_detail(request, user_id):
    employee = get_object_or_404(employees_queryset(), pk=user_id)
    modules = list(Module.objects.filter(is_published=True))
    completions = {
        item.module_id: item.completed_at
        for item in ModuleCompletion.objects.filter(user=employee, module__is_published=True)
    }
    for module in modules:
        module.employee_completed_at = completions.get(module.id)
    total_modules = len(modules)
    completed_count = len(completions)
    return render(request, "onboarding/hr_employee_detail.html", {
        "employee": employee, "modules": modules,
        "completed_count": completed_count, "total_modules": total_modules,
        "progress_percent": round(completed_count / total_modules * 100) if total_modules else 0,
    })
