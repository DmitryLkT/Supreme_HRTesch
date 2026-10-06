from django.db import models
from django.conf import settings

class Module(models.Model):
    title=models.CharField(
        max_length=200,
        verbose_name="Название"
    )

    description=models.TextField(
        verbose_name="Описание"
    )

    order=models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок"
    )

    is_published=models.BooleanField(
        default=False,
        verbose_name="Опубликован"
    )

    content=models.TextField(
        blank=True,
        default="",
        verbose_name="Учебный материал"
    )

    class Meta:
        ordering=['order', 'id']
        verbose_name="Модуль адаптации"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title

class ModuleCompletion(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Сотрудник"
    )

    module=models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        verbose_name="Модуль"
    )

    completed_at=models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата завершения"
    )

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=["user", "module"],
                name="unique_user_module_completion"
            )
        ]

        verbose_name="Завершение модуля"
        verbose_name_plural="Завершение модулей"

    def __str__(self):
        return f"{self.user} — {self.module}"
