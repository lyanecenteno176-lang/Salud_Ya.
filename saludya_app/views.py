from django.shortcuts import render


def index(request):
    return render(request, 'saludya_app/Index.html')


def registro(request):
    return render(request, 'saludya_app/registro.html')


def config_agua(request):
    return render(request, 'saludya_app/config-agua.html')


def config_ejercicios(request):
    return render(request, 'saludya_app/config-ejercicios.html')


def config_medicinas(request):
    return render(request, 'saludya_app/config-medicinas.html')
