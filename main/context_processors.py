from django.conf import settings

def auth_settings(request):
    return {
        'LOGIN_REDIRECT_URL': settings.LOGIN_REDIRECT_URL,
    }