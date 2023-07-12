from django.urls import path
from .views import login_user, logout_user

app_name = 'accounts'

urlpatterns = [
    path(route='login', view=login_user, name="login"),
    path(route='logout', view=logout_user, name="logout"),
]