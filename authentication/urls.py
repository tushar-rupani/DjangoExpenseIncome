from .views import *
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views


urlpatterns = [


	path('register', RegistrationView.as_view(), name='register'),
	path('logout', LogoutView.as_view(), name='logout'),
	path('login', LoginView.as_view(), name='login'),
	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="authentication/reset-password.html"), name="reset_password"),
	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
	path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
	path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
	path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate')




	
]