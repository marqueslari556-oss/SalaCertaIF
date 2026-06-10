from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from app.views import login_view, dashboard, logout_view

urlpatterns = [
    path('', lambda request: redirect('login')),  # Redireciona raiz para login
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
]