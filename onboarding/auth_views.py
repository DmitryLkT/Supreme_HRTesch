from django.contrib.auth.views import LoginView
from django.urls import reverse

from .permissions import is_hr


class RoleLoginView(LoginView):
    template_name = "onboarding/login.html"

    def get_success_url(self):
        # По выбранному правилу роль имеет приоритет над параметром next.
        if self.request.user.is_superuser:
            return reverse("admin:index")
        if is_hr(self.request.user):
            return reverse("hr_dashboard")
        return reverse("home")
