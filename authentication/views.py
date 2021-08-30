from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
# Create your views here.

class RegistrationView(View):
	def get(self, request):
		return render(request, 'authentication/register.html')

	def post(self, request):
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']

		context = {

			'fieldValue' : request.POST

		}


		if not User.objects.filter(username=username).exists():
			if not User.objects.filter(email=email).exists():
				if len(password) < 6 :
					messages.error(request, "Password Should Be More Than 6 letters.")
					return render(request, 'authentication/register.html', context)
					
				user = User.objects.create_user(username=username, email=email)
				user.set_password(password)
				user.is_active = False
				user.save()

				uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

				domain = get_current_site(request).domain

				link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})

				activate_url = "http://" + domain + link

				emailSubject = "Activate Your Account!"
				emailBody = "Hi, " + user.username + "Please use this link to active your Account!\n" + activate_url

				email = EmailMessage(
			    emailSubject,
			    emailBody,
			    'tushar24081@gmail.com',
			    [email],
			   
				)
				email.send(fail_silently = False)
				messages.success(request,"Account Created, Check your email and Activate Account!")



		return render(request, 'authentication/register.html')


class UsernameValidationView(View):
	def post(self, request):
		data = json.loads(request.body)
		username = data['username']

		if not str(username).isalnum():
			return JsonResponse({'user_error': 'Username Wrong!'}, status = 400)
		if User.objects.filter(username = username).exists():
			return JsonResponse({'user_error': 'Username Already Taken'}, status = 409)


		return JsonResponse({'username_valid': True})


class EmailValidationView(View):
	def post(self, request):
		data = json.loads(request.body)
		email = data['email']

		if not validate_email(email):
			return JsonResponse({'email_error': 'Email Wrong!'}, status = 400)
		if User.objects.filter(email = email).exists():
			return JsonResponse({'email_error': 'Email Already Taken'}, status = 409)


		return JsonResponse({'email_valid': True})


class VerificationView(View):
	def get(self, request, uidb64, token):

		
			id = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk = id)

			if not token_generator.check_token(user, token):
				return redirect('login')

			if user.is_active:
				return redirect('login')

			user.is_active = True
			user.save()

			messages.success(request, 'Account Activated')
			return redirect('login')

		

			


class LoginView(View):
	def get(self, request):
		return render(request, 'authentication/login.html')
	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']

		if username and password:
			user = auth.authenticate(username = username, password=password)

			if user:
				if user.is_active:
					auth.login(request, user)
					messages.success(request, "You are now logged in as a " + user.username + "Welcome.")
					return redirect('expenses')

				messages.error(request, "Error occured!")
				return redirect('login')

			messages.error(request, "User is not activated!")
			return redirect('login')
		messages.error(request, "Enter Userid and Password")
		return redirect('login')

class LogoutView(View):
	def post(self, request):
		auth.logout(request)
		return redirect('login')
		messages.success(request, "You are now logged out!")

class RequestPasswordResetEmail(View):

	def get(self, request):
		return render(request, 'authentication/reset-password.html')

	def post(self, request):

		email = request.POST['email']
		context = {
		'values' : request.POST
		}

		if not validate_email(email):
			messages.error(request, "This does not look like appropriate Email.")
			return render(request, 'authentication/reset-password.html')
		




		
