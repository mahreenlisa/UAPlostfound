from django.contrib import admin
from django.urls import path, include
from items import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # login page will show first
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
]
