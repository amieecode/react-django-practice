from django.urls import path
from .views import ( 
    register_user, login_user, logout_user, 
    password_reset_request, password_reset_confirm, get_user_profile, update_user_profile
)

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'), 
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name="password_reset_confirm"),
    path('profile/', get_user_profile, name='user_profile'),
    path('profile/update/', update_user_profile, name='update_user_profile'),
]
