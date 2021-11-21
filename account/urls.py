from django.urls import path, include
from account import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'account'

urlpatterns = [

    #users
    path('user/add_user/', views.add_user),
    path('user/add_admin/', views.add_admin),
    path('user/all_users/', views.get_user),
    path('user/profile/', views.user_detail),
    path('user/reset_password/', views.reset_password),

    path('user/<uuid:user_id>/', views.get_user_detail),
    

    #user login
    path('login/', views.user_login),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    
    #social auth 
    # path('social/', include('social_auth.urls'), name="social-login" ),
    
    path('forget_password/', include('django_rest_passwordreset.urls', namespace='forget_password')),
    
    path('verify_otp/', views.otp_verification),
    path('get_otp/', views.send_otp),

]

