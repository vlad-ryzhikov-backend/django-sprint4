from django.contrib.auth import views
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from blog.views import RegistrationView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/registration/', RegistrationView.as_view(), name='registration'),
    path('auth/', include("django.contrib.auth.urls")),
    path('pages/', include('pages.urls')),
    path('', include('blog.urls', namespace='blog')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

