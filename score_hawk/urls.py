"""
URL configuration for score_hawk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from scores import views

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.home, name='home'),
    path('news/', views.news, name='news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('stats/', views.stats, name='stats'),
    path('players/', views.player_search, name='player_search'),
    path('players/<int:player_id>/', views.player_details, name='player_details'),
    path('rankings/', views.rankings, name='rankings'),
    path('matches/', views.matches, name='matches'),
    path('matches/<int:match_id>/', views.match_details, name='match_details'),
    path('weather/', views.weather, name='weather'),
    path('venues/', views.venues, name='venues'),
    path('compare/', views.compare, name='compare'),
    path('photos/', views.photos, name='photos'),
    path('api_stats/', views.api_stats, name='api_stats'),
    path('cache_stats/', views.cache_stats, name='cache_stats'),
    path('api/cache/refresh/', views.refresh_cache_api, name='refresh_cache_api'),
    path('api/cache/cleanup/', views.cleanup_cache_api, name='cleanup_cache_api'),
]
