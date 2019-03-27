# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action
# from rest_framework.views import APIView

from accounts.models import Profile
from accounts.serializers import ProfileSerializer


# Create your views here.
class ProfileViewset(viewsets.ModelViewSet):
    """
    API View for Profile
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        owner = self.request.user

        if Profile.objects.filter(user_id=owner.id).exist():
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
        return serializer.save(owner=self.request.user)

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


@csrf_exempt
def profile_list(request):
    """
    List all code profile, or create a new snippet.
    """
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def profile_detail(request, pk):
    """
    Retrieve, update or delete a profile.
    """
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(profile, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        profile.delete()
        return HttpResponse(status=204)
