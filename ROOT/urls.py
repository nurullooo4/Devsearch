from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_main.urls')),
    path('accounts/', include('app_users.urls')),

    # Social oauth
    path('social-auth/', include('social_django.urls', namespace='social')),

    # Forget password
    path('password-reset/', PasswordResetView.as_view(template_name='password-reset/password-reset.html'),
         name='password_reset'),
    path(
        'password-reset/done/',PasswordResetDoneView.as_view(template_name='password-reset/password-reset-done.html'),
        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password-reset/password-reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='password-reset/password-reset-complete.html'), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
