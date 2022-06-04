from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView


if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'),
]
urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
