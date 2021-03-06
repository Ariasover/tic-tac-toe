"""Core URLs."""
# Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.users.urls', 'users'), namespace='users')),
    path('', include(('apps.game_core.urls', 'game_core'), namespace='game_core')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
