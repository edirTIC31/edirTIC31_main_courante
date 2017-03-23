from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .utils import is_operator


class OperatorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return is_operator(self.request.user)

    def get_login_url(self):
        if not self.request.user.is_authenticated():
            return super().get_login_url()
        else:
            raise PermissionDenied
