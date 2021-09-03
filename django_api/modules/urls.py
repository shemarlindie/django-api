from django.urls import include, path


urlpatterns = [
    path('polls/', include('django_api.modules.polls.urls')),
]
