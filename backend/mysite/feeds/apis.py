from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, generics, mixins
from rest_framework.response import Response
from rest_framework.authentication import (
    SessionAuthentication, TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from feeds.models import Feed, Comment, Emotion
from feeds.paginations import FeedPagination
from feeds.permissions import IsCommentOwner
from feeds.serializers import (
    FeedSerializer, CommentSerializer, EmotionSerializer)
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

    def get(self, request, pk, format=None):
        feed = get_object_or_404(Feed, pk=pk)
        serializer = FeedSerializer(feed)
        return Response(serializer.data)


# Generic Views
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    pagination_class = CommonPagination

    # It works
    # def post(self, request, *args, **kwargs):
    #     serializer = CommentSerializer(data=request.data)

    #     # get feed
    #     feed = get_feed(request.data['feed_id'])

    #     if serializer.is_valid():
    #         serializer.save(user=request.user, feed=feed)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # It works
    # def create(self, request, *args, **kwargs):
    #     serializer = CommentSerializer(data=request.data)

    #     # get feed
    #     feed = get_feed(request.data['feed_id'])

    #     if serializer.is_valid():
    #         serializer.save(user=request.user, feed=feed)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # it works
    def perform_create(self, serializer):
        data = self.request.data
        feed_id = data.get('feed_id', None)

        # check feed exist
        feed = get_feed(feed_id)

        serializer.save(user=self.request.user, feed=feed)


class CommentDetail(APIView):
    """
    Retrieve, update or delete a comment instance
    """
    authentication_classes = (
        SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, IsCommentOwner)

    def get(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    # Update comment
    def put(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmotionDetail(
        mixins.CreateModelMixin, mixins.DestroyModelMixin,
        mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        feed_id = self.kwargs.get('pk')

        # check feed exist
        feed = get_feed(feed_id)

        emotion = serializer.save(user=self.request.user)

        feed.emotion.add(emotion)
        feed.save()
