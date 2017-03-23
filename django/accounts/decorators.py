from functools import wraps

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

from ipware.ip import get_ip

from .utils import is_operator, passless_login_allowed


def operator_required(function):
    def check_is_operator(user):
        if user.is_authenticated():
            if is_operator(user):
                return True
            else:
                raise PermissionDenied
        else:
            return False
    decorator = user_passes_test(check_is_operator)
    if function:
        return decorator(function)
    return decorator


def passless_ip_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        ip = get_ip(request)
        if passless_login_allowed(ip):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view
