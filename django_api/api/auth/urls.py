from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, GroupViewSet, AuthView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'groups', GroupViewSet, 'groups')

app_name = 'auth_api'

urlpatterns = [
    path('', include(router.urls)),
    path('check/', AuthView.as_view()),
    path('', include('knox.urls')),
]
