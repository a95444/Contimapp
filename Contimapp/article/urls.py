from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views



app_name='article'

urlpatterns = [
    #path('', views.home ,name="home"),
    path('<int:id>/', views.detail, name='detail')    #o id vai ser enviado para a função detail
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)