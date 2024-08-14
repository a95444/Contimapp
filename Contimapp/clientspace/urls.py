from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views #impo
from django.conf import settings
from django.conf.urls.static import static



app_name='clientspace'

urlpatterns = [
    path('', views.clientspace, name='clientspace'),
    path('perfil/', views.update_profile, name='update_profile'),
    path('upload/', views.upload_file, name='upload_file'),
    path('download_certidao/<str:certidao>/', views.view_AT, name='view_AT'),
    path('download_certidaoSS/<str:certidao>/', views.view_SS, name='view_SS'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('clear_task_result/', views.clear_task_result, name='clear_task_result'),
    path('modaltest/', views.modaltest, name='modaltest'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)