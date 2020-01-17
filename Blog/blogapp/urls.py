from django.urls import path
from .views import home, user_signup, user_login, user_logout, show_blogs, create_blog, user_profile

urlpatterns = [
    path('home',home,name='home'),
    path('signup',user_signup,name='signup'),
    path('login',user_login,name='login'),
    path('logout',user_logout,name='logout'),
    path('show-blogs',show_blogs,name='show_blogs'),
    path('create-blog',create_blog,name='create_blog'),
    path('profile',user_profile,name='user_profile'),
]