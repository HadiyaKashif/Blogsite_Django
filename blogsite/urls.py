"""
URL configuration for blogsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/',user_views.profile,name="profile"),
    path('register/',user_views.register,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name = 'login.html',redirect_authenticated_user=True),name="login"), #used the redirect... here so that if a logged in user tries to access login then he can't
    path('logout/',user_views.logoutUser,name="logout"), #not same as I did for login and as in video because for logout that feature is deprecated since it was not secure for users.
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name = 'password_reset.html'),name="password_reset"),
    path('password-reset/done',auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'),name="password_reset_confirm"),
    #uidb64 is userid encoded in base64 and token is the token to check if password is valid
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'),name="password_reset_complete"),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('', include('blog.urls')),
]

if settings.DEBUG:  #not for production just for creating, for deployment method is different see documentation
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)