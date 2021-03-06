""" User's Views """

# Django 
from django.contrib.auth import authenticate,logout,login
from django.views.generic import View,ListView,UpdateView,CreateView,DeleteView,DetailView
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from django.contrib import messages

from django.http import FileResponse
from django.conf import settings
from django.contrib.auth import get_user_model

# For Email conf
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from conf.settings import EMAIL_HOST_USER

# Forms
from ..forms import SignUpForm
# Utils

from apps.utils.tokens import account_activation_token

# Models
User = get_user_model()


class LoginView(View):
	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

			else:
				return HttpResponse("Inactive user.")
		else:
			return HttpResponseRedirect(settings.LOGIN_URL)

		return render(request, "index.html")
	def get(self, request, **kwargs):     
		print(request)
		return render(request, 'login.html')


class LogoutView(View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect(settings.LOGIN_URL)


class IndexView(TemplateView):
	template_name = 'index.html'
	paginate_by = 5
	no_of_message = 1
			
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(pk=self.request.user.pk)

		context.update({
			'user': user,
		})
		
		return context

        
class SignUpView(CreateView):
	form_class = SignUpForm
	template_name = 'signup.html'
	
	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False # Deactivate account till it is confirmed
			user.username = user.email # Deactivate account till it is confirmed
			user.save()

			try:
				"""Send account verification link"""
				current_site = get_current_site(request)
				subject = 'Hi {}, please verify your account'.format(user.email)
				from_email = 'TicTacBomb <noreply@tictacbomb.com>'
				text_content = 'TicTacBomb <noreply@tictacbomb.com>'
				message = render_to_string('account_activation_email.html', {
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': account_activation_token.make_token(user),
				})
				msg = EmailMessage(subject, message, from_email, [user.email])
				msg.content_subtype = 'html'
				msg.send()
			except Exception as e:
				print('error',e)
			return HttpResponseRedirect(reverse('users:email_confirm'))


		return render(request, self.template_name, {'form': form})


class ActivateAccount(View):
	def get(self, request, uidb64, token, *args, **kwargs):
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None

		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.email_confirmed = True
			user.save()
			login(request, user)
			messages.success(request, ('Your account have been confirmed.'))
			return HttpResponseRedirect(reverse('users:index'))
		else:
			messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
			return HttpResponseRedirect(reverse('users:login'))


class EmailConfirmView(TemplateView):
	def get(self, request, **kwargs):     
		return render(request, 'email_confirm.html')

	