from django.contrib.auth.models import User
from django.http import Http404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, generics, mixins, filters
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication, TokenAuthentication)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import Profile
from accounts.paginations import ProfilePagination
from accounts.serializers import (
    ProfileSerializer, UserSerializer, CreateUserSerializer)


class ProfileList(generics.ListAPIView):
    """
    List all profiles, or create a new profile
    """
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    ordering_fields = ('user__first_name', 'user__username')
    ordering = ('user__first_name',)
    pagination_class = ProfilePagination

    # def get_queryset(self):
    #     queryset = Profile.objects.select_related('user').all()
    #     # Set up eager loading to avoid N+1 selects
    #     # queryset = self.get_serializer_class().setup_eager_loading(queryset)
    #     return queryset

    # def get(self, request, format=None):
    #     profiles = Profile.objects.select_related('user').all()
    #     serializer = ProfileSerializer(profiles, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetail(APIView):
    """
    Retrieve, update or delete a profile instance
    """
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Generic Views
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    search_fields = ('username', 'email')
    ordering_fields = ('username', 'email')
    ordering = ('username',)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
