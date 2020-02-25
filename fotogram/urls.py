from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.type, name='signup'),
    path('', views.dashboard, name='dashboard'),
    path('customer', views.customersignup, name='custom_signup'),
    path('photographer', views.photographersignup, name='photographer_signup'),
    path('album/', views.addalbum, name='add-album'),
    path('album/<int:album_id>/photo/add', views.addphoto , name='add-photo'),
    path('album/photo/view/<int:photo_id>', views.viewphoto, name='view-photo'),
    path('album/photo/view/<int:photo_id>/addcomment', views.addcomment, name='add-comment'),
    path('album/<int:album_id>/photo/view/<int:photo_id>/viewcomment', views.viewcomment, name='view-comment'),
    path('album/<int:album_id>/photo/view/<int:photo_id>/like', views.addlike, name='like'),
]
