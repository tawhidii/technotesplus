from django.urls import path
from .views import (
    register,
    ActivateAccount,
    user_login
)

app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name="login"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

]
