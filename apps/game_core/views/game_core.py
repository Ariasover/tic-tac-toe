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
from django.utils.encoding import force_bytes,force_text
from django.contrib import messages

from django.http import FileResponse
from django.conf import settings
from django.contrib.auth import get_user_model

# Models
User = get_user_model()


class GameRoomView(TemplateView):
    	template_name = 'game_room.html'


class ScoreView(TemplateView):
	template_name = 'score.html'


