from django.contrib import admin
from django.urls import path, include
from items import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('post_lost/', views.post_lost_item, name='post_lost_item'),
    path('post_found/', views.post_found_item, name='post_found_item'),
    path('claim-item/<int:item_id>/', views.claim_item, name='claim_item'),
    path('', include('items.urls')),  # ✅ this line connects items/urls.py
]
