from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter

from . import views
from .api_views import ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='api-projects')
router.register('tasks', TaskViewSet, basename='api-tasks')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.project_update, name='project_update'),

    path('projects/<int:project_id>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),

    path('api/', include(router.urls)),
]