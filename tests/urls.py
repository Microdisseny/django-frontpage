from django.contrib import admin
from django.urls import path

from frontpage.views import FrontpageView

urlpatterns = [
    path('', FrontpageView.as_view(), name='frontpage'),
    path('admin/', admin.site.urls),
]
