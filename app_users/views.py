from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth import get_user_model, logout
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator

from app_users.forms import UserRegistrationForm, UserEditForm
from app_main.models import Message, Project
from app_users.models import Skill
from app_users.forms import SkillForm
from app_main.forms import ProjectForm

User = get_user_model()

class UserRegistrationView(CreateView):
    model = User
    template_name = 'app_users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

def logout_view(request):
    logout(request)
    return redirect('login')


class AccountView(DetailView):
    model = User
    template_name = 'app_users/account.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'account'

class CreateSkillView(CreateView):
    model = Skill
    template_name = 'form.html'
    form_class = SkillForm

    def form_valid(self, form):
        skill = form.save(commit=False)
        skill.owner = self.request.user
        skill.save()
        return redirect('account', user_id=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_text'] = 'Create skill'
        return context

    def get_success_url(self) ->str:
        return reverse('account', user_id=self.request.user.id)

class UpdateSkillView(UpdateView):
    model = Skill
    template_name = 'form.html'
    form_class = SkillForm
    pk_url_kwarg = 'skill_id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_text'] = 'Update skill'
        return context

    def get_success_url(self) ->str:
        return reverse('account', kwargs={'user_id':self.request.user.id})

class DeleteSkillView(DeleteView):
    model = Skill
    template_name = 'delete.html'
    pk_url_kwarg = 'skill_id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['confirmation_text'] = (f'Are you sure to delete "{self.get_object().name}" ?')
        return context

    def get_success_url(self) ->str:
        return reverse('account', kwargs={'user_id':self.request.user.id})

class UpdateAccountView(UpdateView):
    model = User
    template_name = 'form.html'
    form_class = UserEditForm
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('account')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_text'] = 'Update account'
        return context

    def get_success_url(self):
        return reverse('account', kwargs={'user_id':self.request.user.id})


def inbox_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(receiver=user).order_by('is_read', '-created_at')

    unread_messages = Message.objects.filter(receiver=user, is_read=False).order_by('-created_at')
    read_messages = Message.objects.filter(receiver=user, is_read=True).order_by('-created_at')
    messages.filter(is_read=False).update(is_read=True)


    context = {
        'user': user,
        'messages': messages,
        'unread_messages': unread_messages,
        'read_messages': read_messages,
    }

    return render(request, 'app_users/inbox.html', context)

class UpdateProjectView(UpdateView):
    model = Project
    template_name = 'form.html'
    form_class = ProjectForm
    pk_url_kwarg = 'project_id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['btn_text'] = 'Update project'
        return context

    def get_success_url(self) ->str:
        return reverse('account', kwargs={'user_id':self.request.user.id})

class DeleteProjectView(DeleteView):
    model = Project
    template_name = 'delete.html'
    pk_url_kwarg = 'project_id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['confirmation_text'] = (f'Are you sure to delete "{self.get_object().name}" ?')
        return context

    def get_success_url(self) ->str:
        return reverse('account', kwargs={'user_id':self.request.user.id})

