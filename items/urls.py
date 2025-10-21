from django.contrib import admin
from django.urls import path
from items import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # login page is shown first
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('post_lost/', views.post_lost_item, name='post_lost_item'),
    path('post_found/', views.post_found_item, name='post_found_item'),
    path('claim-item/<int:item_id>/', views.claim_item, name='claim_item'),
    path('get-questions/<int:found_item_id>/', views.get_questions, name='get_questions'),
]
