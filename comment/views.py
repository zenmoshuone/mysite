from django.shortcuts import render, redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from .forms import CommentForms


def update_commetn(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForms(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        # 检查通过，保存数据,评论
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        # 回复
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user

        comment.save()
        # 返回数据，给前端
        data['status'] = 'SUCCESS'  # 评论成功返回'SUCCESS' 按F12,找到Console,可以看到
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.timestamp()  # 时间戳
        data['text'] = comment.text
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status'] = 'ERROR'  # 失败返回'SUCCESS'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
