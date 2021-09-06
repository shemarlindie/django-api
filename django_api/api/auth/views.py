from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwnUserProfile, IsCreateView, IsStaff
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows auth to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsStaff | IsOwnUserProfile | IsCreateView]
    search_fields = ['first_name', 'last_name', 'username', 'email']


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsStaff]


class AuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        raise exceptions.NotAuthenticated('Not logged in')
