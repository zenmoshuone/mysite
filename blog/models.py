from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # 富文本编辑
from ckeditor_uploader.fields import RichTextUploadingField  # 上传图片
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import ReadNumExpandMethod, ReadDetail

class BlogType(models.Model):
    # 文章分类
    type_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.type_name}'

class Blog(models.Model,ReadNumExpandMethod):
    # 博客文章
    title = models.CharField(max_length=50)  # 文章标题
    # content = RichTextField()  #'ckeditor',富文本编辑修改字段
    content = RichTextUploadingField(verbose_name='博客内容')  # 上传图片要改成这个字段
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 作者
    created_time = models.DateTimeField(auto_now_add=True)  # 发布时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    read_details = GenericRelation(ReadDetail, verbose_name='博客类型')
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)  # 文章分类

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = [
            '-created_time'
        ]