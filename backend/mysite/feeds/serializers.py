from rest_framework import serializers

from accounts.serializers import UserSerializer


class EmotionSerializer(serializers.serializer):
    user = UserSerializer()
    name = serializers.CharField(max_length=100)


class FeedSerializer(serializers.Serializer):
    user = UserSerializer()
    content = serializers.CharField(max_length=255)
    # created = serializers.DateTimeField()
    emotions = EmotionSerializer(many=True)  # A nested list of 'edit' items.


class CommentSerializer(serializers.Serializer):
    user = UserSerializer()
    content = serializers.CharField(max_length=255)
    feed = FeedSerializer()
