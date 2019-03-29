# import json

from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from accounts.models import Profile
from accounts.serializers import ProfileSerializer, UserSerializer


# Create your views here.
class ProfileViewset(viewsets.ModelViewSet):
    """
    API View for Profile
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related('user').all()
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if Profile.objects.filter(user_id=user.id).exists():
            return Response(
                data={'message': 'You had existed an profile'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        user_id = request.user.id
        try:
            my_profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response(
                data={'error': 'User still not create personal profile!'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(my_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileList(APIView):
    """
    List all profiles, or create a new profile
    """
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Profile.objects.select_related('user').all()
        # Set up eager loading to avoid N+1 selects
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def get(self, request, format=None):
        profiles = Profile.objects.select_related('user').all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

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
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
