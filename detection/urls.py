from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_video, name='select_video'),  # Videoyu seçme sayfası
    path('upload_video/', views.upload_video, name='upload_video'),  # Video yükleme işlevi
    path('watch/<str:video_name>/', views.watch_video, name='watch_video'),
    path('videos/', views.list_videos, name='list_videos'),
    path('motions/', views.motion_list, name='motion_list'),
    path('motion/create/', views.create_motion, name='create_motion'),
    path('motion/update/<int:motion_id>/', views.motion_update, name='motion_update'),
    path('motion/delete/<int:motion_id>/', views.motion_delete, name='motion_delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)