"""
URL configuration for myproject project.

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
# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view  # Import the home view if you've created it
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),                     # Admin interface
    path('accounts/', include('accounts.urls')),         # Include all accounts-related URLs
    path('', home_view, name='home'),                    # Root URL pointing to the home view
]

# Configure URL patterns to serve media files in development
if settings.DEBUG:  # Only add this in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

