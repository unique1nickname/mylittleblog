from rest_framework import serializers
from .models import Post, UserComments, UserLikes


class PostSerializer(serializers.ModelSerializer):
    # is_liked = serializers.BooleanField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'text',
            'like_count',
            'comment_count',
            'comments',
            'created_at',
            'updated_at',
            'is_liked',
        )
        read_only_fields = (
            'user',
            'like_count',
            'comment_count',
            'comments',
            'is_liked'
        ) # закончиь писать
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserLikes.objects.filter(user=user, post=obj).exists()

 
#  а этому вообще нужен сериалайзер?? удалить если не пригодится
# вообще - нужен для get по лайкам поста
# class UserLikesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserLikes
#         fields = ('pk', 'user', 'post')
#         read_only_fields = ('user', 'post')


class UserCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComments
        fields = ('id', 'user', 'post', 'text', 'created_at', 'updated_at')
        read_only_fields = ('user', 'post')
