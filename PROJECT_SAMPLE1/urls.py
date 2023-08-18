'''
Team Members
Manmeet Kaur - C0884039
Angrej Singh - C0884026
Riya Sidhu - C0886435
Dheepasri Ravichandran - C0883900
'''
from django.urls import path
from . import views
from .views import CustomLoginView

# URL patterns for the application
urlpatterns = [
    path('base/', views.base_view, name='base'),
    path('', views.MainPageView.as_view(), name='main-page'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('quiz/', views.QuizView.as_view(), name='quiz'),
    path('score/', views.ScoreView.as_view(), name='score'),
    path('review/<int:quiz_id>/', views.ReviewQuizView.as_view(), name='review_quiz'),
]



