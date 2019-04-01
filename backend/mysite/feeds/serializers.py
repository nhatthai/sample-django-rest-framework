from rest_framework import serializers

from accounts.serializers import UserSerializer
from feeds.models import Feed, Comment, Emotion


class EmotionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Emotion
        fields = ('__all__')


class FeedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    content = serializers.CharField(max_length=255)
    created = serializers.DateTimeField(required=False)
    emotions = EmotionSerializer(many=True, required=False)  # A nested list of 'edit' items.

    class Meta:
        model = Feed
        fields = ('id', 'content', 'user', 'created', 'emotions')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    content = serializers.CharField(max_length=255)
    feed = FeedSerializer(read_only=True)
    created = serializers.DateTimeField(required=False)

    class Meta:
        model = Comment
        fields = ('content', 'user', 'feed', 'created')
