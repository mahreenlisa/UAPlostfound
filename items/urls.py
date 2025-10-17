from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_found_item, name='post_found_item'),
    path('post-lost/', views.post_lost_item, name='post_lost_item'),
    path('claim/<int:item_id>/', views.claim_item, name='claim_item'),
]
