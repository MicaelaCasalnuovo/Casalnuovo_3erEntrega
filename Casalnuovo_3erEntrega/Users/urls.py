
from django.urls import path
from Users import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", views.login_request, name="Login"),
    path("register/", views.register, name="Register"),
     path("gracias-por-visitar/", views.gracias_por_visitar, name="GraciasPorVisitar"),
    path("logout/", views.CustomLogoutView.as_view(), name="Logout"),  # Usamos la vista basada en clase para el logout
]