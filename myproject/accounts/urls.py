from django.urls import path
from .views import register_view, login_view, logout_view, home_view, upload_signature  # Make sure to import your view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),  # This is your main home view
    path('upload/', upload_signature, name='upload_signature'),  # Dedicated URL for upload signature
]
