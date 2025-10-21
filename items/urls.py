from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('post_lost/', views.post_lost_item, name='post_lost_item'),
    path('post_found/', views.post_found_item, name='post_found_item'),
    path('claim-item/<int:item_id>/', views.claim_item, name='claim_item'),
    path('get-questions/<int:found_item_id>/', views.get_questions, name='get_questions'),
]
