from django.urls import path

from . import views

urlpatterns = [
    path('', views.DevelopersView.as_view(), name='developers'),
    path('project-create/', views.ProjectCreate.as_view(), name='create_project'),
    path('project/<int:project_id>', views.ProjectDetail.as_view(), name='detail_project'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name='profile'),
    path('projects/', views.projects_view, name='projects'),
    path('send-message/<int:receiver_id>', views.handle_message_submission, name='send_message'),

]