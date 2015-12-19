from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as contrib_login
from django.contrib.auth.views import login as contrib_login_view
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from accounts.forms import CreateUserForm


def login_operator(request, username=None):

    form = CreateUserForm()

    if username:

        user = get_object_or_404(User, username=username)

        if user.is_superuser:

            messages.error(request, "Il faut un mot de passe pour se connecter "
                                    "avec cet utilisateur ;-)")
            return redirect('login')

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        contrib_login(request, user)

        redirect_to = request.GET.get(REDIRECT_FIELD_NAME, reverse('login'))

        return redirect(redirect_to)

    c = {
        'create_user_form': form,
        'operators': User.objects.filter(is_superuser=False, is_active=True),
        'next': request.GET.get(REDIRECT_FIELD_NAME, ''),
    }

    return render(request, 'accounts/login_operator.html', c)

def login_administrator(request, *args, **kwargs):

    c = {
        'administrators': User.objects.filter(is_superuser=True),
        'next': request.GET.get(REDIRECT_FIELD_NAME, ''),
    }

    return contrib_login_view(request, *args,
            template_name='accounts/login_administrator.html',
            extra_context=c, **kwargs)

def create_user(request):

    redirect_to = request.GET.get(REDIRECT_FIELD_NAME, reverse('login'))
    form = CreateUserForm(request.POST)

    if request.method != 'POST':
        raise Http404

    if not form.is_valid():
        messages.error(request, 'Ce nom d’utilisateur existe déjà.')
        return redirect(redirect_to) # FIXME

    username = form.cleaned_data['username']
    assert(not User.objects.filter(username=username).exists())

    user = User.objects.create_user(username)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    contrib_login(request, user)

    return redirect(redirect_to)
