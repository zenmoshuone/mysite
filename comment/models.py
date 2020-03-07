from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User


# 评论
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 评论的数据
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)  # 评论谁写的

    # 回复评论
    root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.CASCADE)  # 最开始的那条评论,用来获取该评论下的回复
    parent = models.ForeignKey('self', null=True, related_name='parent_comment',
                               on_delete=models.CASCADE)  # self指向自己,回复那条评论
    reply_to = models.ForeignKey(User, null=True, related_name='replies', on_delete=models.CASCADE)  # 回复谁

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']