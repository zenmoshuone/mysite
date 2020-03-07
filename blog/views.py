from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.db.models import Count
from django.conf import settings
from read_statistics.utils import read_statistics_once_read


# 公共函数
def contrl(request, blogs):
    page_num = request.GET.get('page', 1)  # 获得？后面字典里的内容(都是字符串)，如果没有，默认为第一页
    paginator = Paginator(blogs, settings.EACH_PAGE_BLOGS_NUMBER)
    # django自带的get_page，可以自动帮我们处理获得的数字， # 如果用户输入的是其他内容，自动转换为1
    page_of_blogs = paginator.get_page(page_num)  # 根据页码获得具体的页面
    currentr_page_num = page_of_blogs.number  # 获取当前页面
    page_range = list(range(max(1, currentr_page_num - 2), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))  # 显示的页码
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    '''博客分类统计第一种方法
    blog_types = BlogType.objects.all()
    blog_type_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_type_list.append(blog_type)
    '''
    # 第二种
    type_list = BlogType.objects.annotate(blog_count=Count('blog'))  # 分类统计方法2

    # 获取日期归档对应的博客数量
    blogs_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blogs_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blogs'] = blogs
    context['blog_types'] = type_list
    # 获取日期归档对应的博客数量
    context['blog_dates'] = blog_dates_dict  # 日期
    return context


# 博客列表函数
def blog_list(request):
    blogs = Blog.objects.all()
    context = contrl(request, blogs)
    return render(request, 'blog/blog_list.html', context=context)


# 博客类型函数，#根据分类的pk值查找到分类名
def blogs_with_type(request, blogs_with_pk):
    blog_type = get_object_or_404(BlogType, pk=blogs_with_pk)
    blogs = Blog.objects.filter(blog_type=blog_type)
    context = contrl(request, blogs)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


# 博客时间函数，根据创建的时间
def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = contrl(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context=context)


# 博客详情函数
def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)  # 获取cookie标记

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()  # 上一篇
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 下一篇
    context['blog'] = blog
    response = render(request, 'blog/blog_detail.html', context=context)  # 响应
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记  # 设置cookie,是字典,比如第10篇是{'blog_10_readed':true}
    return response
