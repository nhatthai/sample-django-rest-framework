from django.contrib.auth import authenticate, logout
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from accounts.models import Profile
from accounts.serializers import ProfileSerializer


# For login
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def sign_in(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({
            'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({
            'error': 'Invalid Credentials'},
            status=status.HTTP_404_NOT_FOUND)

    existed_token = Token.objects.get(user_id=user.id)
    return Response(
        data={
            'token': existed_token.key,
            'user_id': user.pk, 'email': user.email},
        status=status.HTTP_200_OK)


# For logout
class Logout(APIView):
    def post(self, request, format=None):
        print("request user", request.user)

        if request.user:
            # check user's info and logout
            logout(request)
        else:
            return Response({
                'error': 'You need to login first!'},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class ProfileViewset(viewsets.ModelViewSet):
    """
    API View for Profile
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related('user').all()
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        user = self.request.user

        if Profile.objects.check_profile_exist(user.id):
            return Response(
                data={'message': 'You had existed an profile'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
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
