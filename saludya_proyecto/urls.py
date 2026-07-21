"""
URL configuration for saludya_proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from saludya_app.views import (
    index,
    registro,
    config_agua,
    config_ejercicios,
    config_medicinas,
)

urlpatterns = [
    path('', index, name='index'),
    path('index.html', index, name='index_html'),
    path('registro.html', registro, name='registro'),
    path('config-agua.html', config_agua, name='config_agua'),
    path('config-ejercicios.html', config_ejercicios, name='config_ejercicios'),
    path('config-medicinas.html', config_medicinas, name='config_medicinas'),
    path('admin/', admin.site.urls),
]
