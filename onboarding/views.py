from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Module, ModuleCompletion


@login_required
def home(request):
    modules = Module.objects.filter(is_published=True)

    completed_module_ids = set(
        ModuleCompletion.objects.filter(
            user=request.user,
            module__is_published=True,
        ).values_list("module_id", flat=True)
    )

    total_modules = modules.count()
    completed_count = len(completed_module_ids)

    progress_percent = (
        round(completed_count / total_modules * 100)
        if total_modules > 0
        else 0
    )

    context = {
        "page_title": "Твой маршрут адаптации",
        "modules": modules,
        "completed_module_ids": completed_module_ids,
        "total_modules": total_modules,
        "completed_count": completed_count,
        "progress_percent": progress_percent,
    }

    return render(request, "onboarding/home.html", context)


@login_required
def module_detail(request, module_id):
    module = get_object_or_404(
        Module,
        id=module_id,
        is_published=True,
    )

    is_completed = ModuleCompletion.objects.filter(
        user=request.user,
        module=module,
    ).exists()

    context = {
        "module": module,
        "is_completed": is_completed,
    }

    return render(
        request,
        "onboarding/module_detail.html",
        context,
    )


@login_required
@require_POST
def complete_module(request, module_id):
    module = get_object_or_404(
        Module,
        id=module_id,
        is_published=True,
    )

    ModuleCompletion.objects.get_or_create(
        user=request.user,
        module=module,
    )

    return redirect("module_detail", module_id=module.id)