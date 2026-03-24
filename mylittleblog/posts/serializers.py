from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    ...


class UserLikesSerializer(serializers.ModelSerializer):
    ...


class UserCommentsSerializer(serializers.ModelSerializer):
    ...