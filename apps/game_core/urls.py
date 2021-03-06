"""Circles URLs."""

# Django
from django.urls import path

# Views
from .views.game_core import GameRoomView,ScoreView

urlpatterns = [
    path('game/game-room',GameRoomView.as_view(),name="game_room"),
    path('game/score',ScoreView.as_view(),name="score"),
]