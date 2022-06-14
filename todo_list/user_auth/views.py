from django.contrib.auth import login, logout
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from .serializers import NullSerializer, UserSerializer, LoginSerializer, SignupSerializer


class AuthViewSet(viewsets.ModelViewSet):
    """
        Viewset to login/signup/list the User object.
        **Context**
        :class:`django.contrib.auth.models.User` .

        **Permission** : AllowAny
    """
    permission_classes = (AllowAny,)

    # mapping serializer into the action
    serializer_classes = {
        'login': LoginSerializer,
        'signup': SignupSerializer,
        'logout': NullSerializer,
    }

    # default serializer
    default_serializer_class = UserSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @action(methods=['POST', ], detail=False, name='login')
    def login(self, request):
        serializer = self.get_serializer(data=request.data, many=False)
        if serializer.is_valid():
            # get user from serializer data
            user = serializer.validated_data.get("user")
            if user and user.is_active:
                # call Django login method
                login(request, user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST', ], detail=False, name='signup')
    def signup(self, request):
        serializer = self.get_serializer(data=request.data, many=False)
        if serializer.is_valid():
            # get user from serializer data
            user = serializer.validated_data.get("user")
            if user:
                # call Django login method
                login(request, user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET', ], detail=False, name='logout', permission_classes=[IsAuthenticated, ])
    def logout(self, request):
        """
            Calls Django logout method.
        """
        logout(request)
        return Response("successfully logged out", status=status.HTTP_200_OK)
