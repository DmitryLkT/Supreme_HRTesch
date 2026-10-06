from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(
        "modules/<int:module_id>/",
        views.module_detail,
        name="module_detail"
    ),

    path(
        "modules/<int:module_id>/complete/",
        views.complete_module,
        name="complete_module"
    )
]