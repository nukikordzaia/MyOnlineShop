from django.urls import path
from user import views


urlpatterns =[
    path('users/', views.UserList.as_view()),
    path('detail/', views.UserDetail.as_view()),
    path('login/', views.AuthView.as_view()),

]