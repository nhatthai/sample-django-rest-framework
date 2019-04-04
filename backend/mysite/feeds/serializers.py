from rest_framework import serializers

from accounts.serializers import UserSerializer
from feeds.models import Feed, Comment, Emotion


class EmotionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = UserSerializer(read_only=True)
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Emotion
        fields = ('id', 'name', 'user')


class FeedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    content = serializers.CharField(max_length=255)
    created = serializers.DateTimeField(required=False)
    emotion = EmotionSerializer(many=True, required=False)

    class Meta:
        model = Feed
        fields = ('id', 'content', 'user', 'created', 'emotion')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    content = serializers.CharField(max_length=255)
    feed = FeedSerializer(read_only=True)
    created = serializers.DateTimeField(required=False)

    class Meta:
        model = Comment
        fields = ('content', 'user', 'feed', 'created')
