from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, generics
from rest_framework.response import Response
from rest_framework.authentication import (
    SessionAuthentication, TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from feeds.models import Feed, Comment
from feeds.paginations import FeedPagination
from feeds.serializers import FeedSerializer, CommentSerializer
from commons.paginations import CommonPagination

from .utils import get_feed


# Generic Views
class FeedList(generics.ListCreateAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    pagination_class = FeedPagination

    def post(self, request, *args, **kwargs):
        serializer = FeedSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedDetail(APIView):
    """
    Retrieve, update or delete a feed instance
    """
    authentication_classes = (
        SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


# Generic Views
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = FeedSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    pagination_class = CommonPagination

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)

        # get feed
        feed = get_feed(request.data['feed_id'])

        if serializer.is_valid():
            serializer.save(user=request.user, feed=feed)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
