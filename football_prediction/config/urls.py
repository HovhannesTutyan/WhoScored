from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.teams.urls')),
    path('api/', include('apps.players.urls')),
    path('api/', include('apps.comparison.urls')),
    path('api/', include('apps.prediction.urls')),
    path('api/', include('apps.ratings.urls')),
    path('api/', include('apps.analytics.urls')),
]
