from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views, logout
from . import views
from .forms import LoginForm



app_name='core'

urlpatterns = [
    path('', views.home ,name="home"),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('/artigo', views.XXXX, name="detail")

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




#    path('contacto/', views.contact, name='contact'), #passou-se do puddle para aqui


#este url file deverá ser importado para o url file principal
#o fic URLs principal reencaminha para aqui os urls com items/ e depois isto vai ver se tem uma primary key depois de items/XXXX