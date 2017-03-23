from functools import wraps

from django.core.exceptions import PermissionDenied

from ipware.ip import get_ip

from .utils import passless_login_allowed


def passless_ip_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        ip = get_ip(request)
        if passless_login_allowed(ip):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view
