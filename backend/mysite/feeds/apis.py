from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, generics, mixins
from rest_framework.authentication import (
    SessionAuthentication, TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
    queryset = Feed.objects.select_related(
        'user').prefetch_related('emotion', 'emotion__user').all()
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
        feed = self.get_queryset()
        serializer = FeedSerializer(feed)
        return Response(serializer.data)

    def get_queryset(self):
        return Feed.objects.select_related('user').prefetch_related(
            'emotion', 'emotion__user').get(pk=self.kwargs.get('pk'))


# Generic Views
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    pagination_class = CommonPagination

    def perform_create(self, serializer):
        """
        create a comment
        """
        # check feed exist
        feed = get_feed(self.kwargs.get('pk'))
        if feed:
            serializer.save(user=self.request.user, feed=feed)

    def get_queryset(self):
        return self.queryset.select_related(
            'feed', 'feed__user').prefetch_related(
                'feed__emotion').filter(feed_id=self.kwargs.get('pk'))


class CommentDetail(APIView):
    """
    Retrieve, update or delete a comment instance
    """
    serializer_class = CommentSerializer
    authentication_classes = (
        SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, IsCommentOwner)

    def get_queryset(self):
        return Comment.objects.select_related(
            'feed', 'feed__user').prefetch_related(
                'feed__emotion', 'feed__emotion__user').get(
                    id=self.kwargs.get('pk'))

    def get(self, request, pk, format=None):
        comment = self.get_queryset()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    # Update comment
    def put(self, request, pk, format=None):
        comment = self.get_queryset()
        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = get_object_or_404(Comment, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmotionList(generics.ListCreateAPIView):
    queryset = Emotion.objects.select_related('user').all()
    serializer_class = EmotionSerializer
    authentication_classes = (
        SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        feed = get_feed(self.kwargs.get('pk'))
        if feed:
            emotion = serializer.save(user=self.request.user)
            feed.emotion.add(emotion)


class EmotionDetail(
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        generics.GenericAPIView):
    serializer_class = EmotionSerializer
    lookup_field = "id"
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        return Emotion.objects.select_related(
            'user').get(id=self.kwargs["id"])

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_queryset()

        # check exist feed
        if get_feed(self.kwargs.get('pk')):

            serializer = EmotionSerializer(instance, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Emotion, pk=self.kwargs.get('id'))
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
