from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(template_name='app_users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('account/<int:user_id>/', views.AccountView.as_view(), name='account'),
    path('update-account/<int:user_id>/', views.UpdateAccountView.as_view(), name='update_account'),

    path('create-skill/', views.CreateSkillView.as_view(), name='create_skill'),
    path('update-skill/<int:skill_id>/', views.UpdateSkillView.as_view(), name='update_skill'),
    path('delete-skill/<int:skill_id>/', views.DeleteSkillView.as_view(), name='delete_skill'),
    path('update-project/<int:project_id>/', views.UpdateProjectView.as_view(), name='update_project'),
    path('delete-project/<int:project_id>/', views.DeleteProjectView.as_view(), name='delete_project'),
    path('inbox/<int:user_id>/', views.inbox_view, name='inbox'),

]