from django.contrib.auth.views import logout as logout_view

def logout(request):
    return logout_view(request, next_page='/')
