"""postanything URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

# This imports have to do with managing images and static files
from django.conf import settings
from django.conf.urls.static import static

# import for the user
from users.views import register
from django.contrib.auth.views import LogoutView
from users.views import login_view, update_user, ProfileDetailView

# Import for password reset
from django.contrib.auth.views import PasswordResetView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('register/', view=register, name='register'),
    path('login/', view=login_view, name='login'),
    path('logout/', view=LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path('update_user/', view=update_user, name='update_user'),
    path('my-profile/<int:pk>', view=ProfileDetailView.as_view(), name="my_profile"),
    # I specify the template_name so that I can tell django where to find this template.
    # Otherwise, it will search for it in the default location.
    path('password-reset/',
        view=PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset")
]

# This conditional will render the images and static files only during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
