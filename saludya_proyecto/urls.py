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
    historial,
    config_agua,
    config_ejercicios,
    config_medicinas,
    perfil,
    progreso,
    gamification_dashboard,
    marketplace,
    market_view,
    product_detail,
    product_create,
    product_edit,
    product_delete,
    category_list,
    category_create,
    category_edit,
    category_delete,
    add_to_cart,
    remove_from_cart,
    cart_view,
    checkout,
    order_history,
    export_orders_pdf,
    habit_create,
    habit_edit,
    habit_delete,
    habit_entry_create,
    habit_entry_list,
    export_progress_pdf,
    redeem_reward,
    api_gamification,
    api_badges,
    api_rewards,
    api_points,
    api_progress,
    api_habits,
    api_products,
    api_orders,
)

urlpatterns = [
    # Páginas principales
    path('', index, name='index'),
    path('index.html', index, name='index_html'),
    path('registro.html', registro, name='registro'),

    
    # Configuración de hábitos

    path('historial/', historial, name='historial'),

    path('config-agua.html', config_agua, name='config_agua'),
    path('config-ejercicios.html', config_ejercicios, name='config_ejercicios'),
    path('config-medicinas.html', config_medicinas, name='config_medicinas'),
    
    # Perfil y progreso
    path('perfil.html', perfil, name='perfil'),
    path('progreso/', progreso, name='progreso'),
    path('gamificacion/', gamification_dashboard, name='gamification'),
    
    # Gestión de hábitos
    path('progreso/habit/create/', habit_create, name='habit_create'),
    path('progreso/habit/<int:habit_id>/edit/', habit_edit, name='habit_edit'),
    path('progreso/habit/<int:habit_id>/delete/', habit_delete, name='habit_delete'),
    
    # APIs de hábitos
    path('api/habit-entry/create/', habit_entry_create, name='habit_entry_create'),
    path('api/habit-entry/list/', habit_entry_list, name='habit_entry_list'),
    
    # APIs de gamificación
    path('api/gamification/', api_gamification, name='api_gamification'),
    path('api/badges/', api_badges, name='api_badges'),
    path('api/rewards/', api_rewards, name='api_rewards'),
    path('api/points/', api_points, name='api_points'),
    path('api/progress/', api_progress, name='api_progress'),
    path('api/habits/', api_habits, name='api_habits'),
    
    # APIs de marketplace
    path('api/products/', api_products, name='api_products'),
    path('api/orders/', api_orders, name='api_orders'),

    # Marketplace - Productos
    path('marketplace/', marketplace, name='marketplace'),

    path('marketplace/', market_view, name='marketplace'),
    path('market/', market_view, name='market'),
    path('marketplace/product/new/', product_create, name='product_create'),

    path('marketplace/product/<int:product_id>/', product_detail, name='product_detail'),
    path('marketplace/product/new/', product_create, name='product_create'),
    path('marketplace/product/<int:product_id>/edit/', product_edit, name='product_edit'),
    path('marketplace/product/<int:product_id>/delete/', product_delete, name='product_delete'),
    
    # Marketplace - Carrito
    path('marketplace/cart/', cart_view, name='cart'),
    path('marketplace/cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('marketplace/cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('marketplace/checkout/', checkout, name='checkout'),
    
    # Marketplace - Categorías
    path('marketplace/categories/', category_list, name='category_list'),
    path('marketplace/category/new/', category_create, name='category_create'),
    path('marketplace/category/<int:category_id>/edit/', category_edit, name='category_edit'),
    path('marketplace/category/<int:category_id>/delete/', category_delete, name='category_delete'),
    
    # Marketplace - Pedidos
    path('marketplace/orders/', order_history, name='order_history'),
    path('marketplace/orders/export/pdf/', export_orders_pdf, name='export_orders_pdf'),
    
    # Exportación y recompensas
    path('export/progreso/pdf/', export_progress_pdf, name='export_progress_pdf'),
    path('reward/redeem/<int:reward_id>/', redeem_reward, name='redeem_reward'),
    
    # Admin
    path('admin/', admin.site.urls),
]
