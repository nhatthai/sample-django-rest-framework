from django.contrib.auth.models import User

from rest_framework import serializers

from accounts.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    address = serializers.CharField(allow_blank=True, max_length=500)
    short_bio = serializers.CharField(allow_blank=True, max_length=255)

    class Meta:
        model = Profile
        fields = ('id', 'address', 'short_bio', 'user')

    @classmethod
    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('user')
        return queryset

    def validate(self, data):
        return data

    def create(self, validated_data):
        address = validated_data.get('address', None)
        short_bio = validated_data.get('short_bio', None)
        user_data = validated_data.pop('user')
        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)

        return Profile.objects.create(
            user_id=user.id,
            short_bio=short_bio,
            address=address)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.short_bio = \
            validated_data.get('short_bio', instance.short_bio)
        instance.save()
        return instance
