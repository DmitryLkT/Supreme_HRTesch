from django.contrib import admin
from .models import Module

class ModuleAdmin(admin.ModelAdmin):
    list_display=[
        "title",
        "order",
        "is_published"
    ]

    list_filter=[
        "is_published"
    ]

    search_fields=[
        "title",
        "description"
    ]

admin.site.register(Module,ModuleAdmin)
