from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('audio-create/', views.audioFileCreate, name="audio-create"),
    path('audio-list/<str:audioFileType>/<str:audioFileID>/', views.audioFileList, name="audio-detail"),
    path('audio-list/<str:audioFileType>/', views.audioFileList, name="audio-list"),
    path('audio-update/<str:audioFileType>/<str:audioFileID>/', views.audioFileUpdate, name="audio-update"),
    path('audio-delete/<str:audioFileType>/<str:audioFileID>/', views.audioFileDelete, name="audio-delete"),
]
