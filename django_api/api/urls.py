from django.urls import path, include

urlpatterns = [
    path('explorer/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('django_api.api.auth.urls')),
    path('polls/', include('django_api.api.polls.urls')),
]
