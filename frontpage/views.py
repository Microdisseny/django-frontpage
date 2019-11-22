from django.conf import settings
from django.contrib.admin.sites import site
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from .utils import replace_next_parameter


class FrontpageView(TemplateView):
    template_name = "frontpage/index.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_prefix = getattr(settings, 'FRONTPAGE_ADMIN_PREFIX', '/admin/')

    def dispatch(self, *args, **kwargs):
        user = getattr(self.request, 'user', None)

        if user is None:
            raise ImproperlyConfigured('AuthenticationMiddleware not in MIDDLEWARE?')

        if user.is_authenticated and user.is_staff:
            return HttpResponseRedirect(self.admin_prefix)

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(site.each_context(self.request))

        next = self.request.GET.get(REDIRECT_FIELD_NAME, self.admin_prefix)

        login_url_name = getattr(settings, 'FRONTPAGE_LOGIN_URL_NAME', 'admin:login')
        login_url = reverse(login_url_name)
        login_url = replace_next_parameter(login_url, next)
        context['login_url'] = self.request.build_absolute_uri(login_url)

        relogin_url_name = getattr(settings, 'FRONTPAGE_RELOGIN_URL_NAME', 'admin:login')
        relogin_url = reverse(relogin_url_name)
        relogin_url = replace_next_parameter(relogin_url, next)
        context['relogin_url'] = self.request.build_absolute_uri(relogin_url)

        return context
