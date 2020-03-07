from django.urls import path
from .views import blog_detail, blog_list, blogs_with_type, blogs_with_date

urlpatterns = [
    path('', blog_list, name="blog_list"),
    path('<int:blog_pk>', blog_detail, name="blog_detail"),
    path('type/<int:blogs_with_pk>', blogs_with_type, name="blogs_with_type"),
    path('date/<int:year>/<int:month>', blogs_with_date, name="blogs_with_date"),
]
