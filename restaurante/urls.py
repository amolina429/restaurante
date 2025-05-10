"""
URL configuration for restaurante project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from main.views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', HomeView.as_view(), name='home'),
    path('quienes-somos/', QuienesSomosView.as_view(), name='quienes_somos'),
    path('contactenos/', ContactenosView.as_view(), name='contactenos'),
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/nueva/', CategoriaCreateView.as_view(), name='categoria-create'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categorias/eliminar/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria-delete'),
    
    # URLs para Platos
    path('platos/', PlatoListView.as_view(), name='plato-list'),
    path('platos/nuevo/', PlatoCreateView.as_view(), name='plato-create'),
    path('platos/editar/<int:pk>/', PlatoUpdateView.as_view(), name='plato-update'),
    path('platos/eliminar/<int:pk>/', PlatoDeleteView.as_view(), name='plato-delete'),

    path('servicios/', ServiciosView.as_view(), name='servicios'),
    path('servicios/mesa/', MesaCreateView.as_view(), name='mesa-create'),
    path('servicios/domicilio/', DomicilioCreateView.as_view(), name='domicilio-create'),
    path('servicios/recoger/', RecogerCreateView.as_view(), name='recoger-create'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)