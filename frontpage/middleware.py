from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

from .utils import redirect_to_url_with_next


class FrontpageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        login_url_name = getattr(settings, 'FRONTPAGE_LOGIN_URL_NAME', 'admin:login')
        self.login_url = reverse(login_url_name)
        logout_url_name = getattr(settings, 'FRONTPAGE_LOGOUT_URL_NAME', 'admin:logout')
        self.logout_url = reverse(logout_url_name)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        admin_prefix = getattr(settings, 'FRONTPAGE_ADMIN_PREFIX', '/admin/')

        user = getattr(request, 'user', None)

        if user is None:
            raise ImproperlyConfigured('Frontpage middleware should appear after AuthenticationMiddleware')

        if (
            request.method == 'GET'
            and request.path.startswith(admin_prefix)
            and not request.path.startswith(self.login_url)
            and not request.path.startswith(self.logout_url)
            and not (request.user.is_authenticated and request.user.is_staff)
        ):
            return redirect_to_url_with_next(self.get_frontpage_url(), request.get_full_path())

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def get_frontpage_url(self):
        url_name = getattr(settings, 'FRONTPAGE_URL_NAME', 'frontpage')
        return reverse(url_name)
