from django.contrib.auth.views import logout as logout_view
from django.core.urlresolvers import reverse

def logout(request):
    return logout_view(request, next_page=reverse('list-evenements'))
