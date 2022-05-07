from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='authenticate-login'),
    path('authentication/register/', views.register_page, name='authenticate-register'),
]

