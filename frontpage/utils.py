from urllib.parse import urlparse, urlunparse

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect, QueryDict


def redirect_to_url_with_next(url, next):
    url = replace_next_parameter(url, next)
    return HttpResponseRedirect(url)


def replace_next_parameter(url, next):
    url_parts = list(urlparse(url))
    querystring = QueryDict(url_parts[4], mutable=True)
    querystring[REDIRECT_FIELD_NAME] = next
    url_parts[4] = querystring.urlencode(safe='/')
    return urlunparse(url_parts)
