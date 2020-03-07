from django import template
from ..models import Comment
from ..forms import CommentForms
from django.contrib.contenttypes.models import ContentType

register = template.Library()


# 自定义模板标签

# 评论数
@register.simple_tag
def get_comment_count(obj):  # obj 需要在模板页面传入参数进来
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()

# 获取评论表单
@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForms(initial={'content_type': content_type.model,
                                 'object_id': obj.pk, 'reply_comment_id': '0'})  # 获取博客的类型和id
    return form

# 获取评论列表
@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')