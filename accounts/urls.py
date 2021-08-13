from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register,
    ActivateAccount,
    user_login,
    user_logout,
    user_profile,
    change_user_password
)


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name="login"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('logout/', user_logout, name='logout'),
    path('change_password/',change_user_password,name='change-password'),
    path('profile/<str:username>/',user_profile,name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done'
                                                                                        '.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts'
                                                                                              '/password_reset_confirm'
                                                                                              '.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete'
                                                                                   '.html'),
         name='password_reset_complete')
]
