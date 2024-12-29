
from django.urls import path
from Users import views
from django.contrib.auth.views import LogoutView
from django.urls import path, include  # Asegúrate de usar 'include'
from . import views


urlpatterns = [
    path("login/", views.login_request, name="Login"),
    path("register/", views.register, name="Register"),
    path("gracias-por-visitar/", views.gracias_por_visitar, name="GraciasPorVisitar"),
    path("logout/", views.CustomLogoutView.as_view(), name="Logout"),
    path('cambiar-email-y-contrasena/', views.cambiar_email_y_contrasena, name='cambiar_email_y_contrasena'),
    path('eliminar_cliente/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('', include('App.urls')),
    path('eliminar-compra/<int:id>/', views.eliminar_compra, name='eliminar_compra'),
     path('eliminar-producto/<str:sku>/', views.eliminar_producto, name='eliminar_producto'),
]