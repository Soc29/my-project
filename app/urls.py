from django.urls import path
from app import views
from .views import LoginView , SignupView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('post/create/', views.CreateView.as_view(), name='create'),
    path('post/<int:pk>/edit/', views.EditView.as_view(), name='edit'),
    path('post/<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    path('category/<str:category>/', views.CategoryView.as_view(), name='category'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView, name='signup'),
   

]
