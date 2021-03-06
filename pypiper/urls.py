"""pypiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('B9CwRbcfAwVMfoVpZYZ6ec8RvLaq7cm3/admin/', admin.site.urls),
    path('', include('gmail_authentication.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('', include('vote.urls')),
    path('web/admin/', include('admin_authentication.urls')),
    path('web/admin/', include('admin_dashboarding.urls')),
    path('web/admin/', include('predictions.urls')),
    path('web/admin/', include('mailer.urls')),
    path('', include('vote_feed.urls')),
    path('', include('profile_feed.urls')),
]
