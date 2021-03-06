"""Users models."""

# Django
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


# Utilities
from apps.utils.models import HistoryModel


class User(HistoryModel, AbstractUser):
	"""User model.
	Extend from Django's Abstract User, change the username field
	to email and add some extra fields.
	"""
	customer_id = models.CharField(max_length=100, blank=True,null=True)
	email = models.EmailField(
		'email address',
		unique=True,
		error_messages={
			'unique': 'A user with that email already exists.'
		}
	)
	# phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	email_confirmed = models.BooleanField(
		'verified',
		default=False,
		help_text='Set to true when the user have verified its email address.'
	)

	def __str__(self):
		"""Return username."""
		return self.username

	def get_short_name(self):
		"""Return username."""
		return self.username

	@property
	def description(self):
		"""Return username."""
		return 'Descripcion para el usuario {}'.format(self.username)
        
admin.site.register(User)
