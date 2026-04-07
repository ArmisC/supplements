from django.urls import path
from . import views
app_name = 'users'


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('<int:pk>/logout/', views.logout, name='logout'),
    path("view-one/", views.view_one, name='view-one'),
    path("view-two/", views.view_two, name='view-two'),
]