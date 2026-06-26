from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('registrar/', views.register_user, name='register'),
    path('productos/', views.productos_list, name='productos'),
    path('producto/<int:pk>/', views.producto_detail, name='producto'),
    path('producto/nuevo/', views.producto_create, name='producto_create'),
    path('producto/editar/<int:pk>/', views.producto_update, name='producto_update'),
    path('producto/eliminar/<int:pk>/', views.producto_delete, name='producto_delete'),
]
