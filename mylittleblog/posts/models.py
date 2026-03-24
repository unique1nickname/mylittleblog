from django.db import models
from django.conf import settings


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=256)
    text = models.TextField()
    like_count = models.PositiveIntegerField()
    comment_count = models.PositiveIntegerField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserLikes", related_name='liked_posts')
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserComments", related_name='commented_posts')
    created_at = models.DateTimeField(auto_now_add=True)


class UserLikes(models.Model):
    pk = models.CompositePrimaryKey("user_id", "post_id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["user", "post"], name="unique_user_post"
    #         ),
    #     ]


class UserComments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
