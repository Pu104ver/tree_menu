from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='base'),
    path('admin/', admin.site.urls),
    path('menu/', include('menu.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
