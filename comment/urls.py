from django.urls import path
from . import views

urlpatterns = [
    path('update_comment/', views.update_commetn, name="update_comment")
]
