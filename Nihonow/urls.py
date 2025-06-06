"""
URL configuration for Nihonow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView
from treasures.sitemaps import StaticViewSitemap
from treasures.views import custom_login, logout_view

# Define the sitemaps dictionary
sitemaps = {
    'static': StaticViewSitemap,
}
# Define custom error handlers
handler400 = 'treasures.views.custom_400'
handler403 = 'treasures.views.custom_403'
handler404 = 'treasures.views.custom_404'
handler500 = 'treasures.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', custom_login, name='login'),
    path('', include('treasures.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('dojo/', include('dojo.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_view, name='logout'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('ads.txt', TemplateView.as_view(template_name="ads.txt", content_type="text/plain")),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)