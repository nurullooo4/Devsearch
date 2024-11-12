from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import ProjectForm, MessageForm
from .models import Project, Tag, Comment

User = get_user_model()


class DevelopersView(ListView):
    template_name = 'app_main/developers.html'
    paginator_class = Paginator
    paginate_by = 3

    def get_queryset(self):
        return User.objects.all()

    context_object_name = 'developers'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        page_obj = context['page_obj']
        left_index = page_obj.number - 1
        right_index = page_obj.number + 1

        if left_index < 1:
            left_index = 1

        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages

        custom_range = range(left_index, right_index + 1)
        context['custom_range'] = custom_range
        return context


class ProjectCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    model = Project
    template_name = 'app_main/project_form.html'
    form_class = ProjectForm
    extra_context = {
        'btn_text': 'Create project'
    }

    def get_success_url(self):
        return reverse('account', kwargs={'user_id': self.request.user.id})

    def form_valid(self, form):
        tags = self.request.POST.get('tags', '').split(',')
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()

        for tag_name in tags:
            tag_name = tag_name.strip().lower()
            tag, created = Tag.objects.get_or_create(name=tag_name)
            project.tags.add(tag)

        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProjectDetail(DetailView):
    model = Project
    template_name = 'app_main/project.html'
    pk_url_kwarg = 'project_id'

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        comment = request.POST.get('comment')

        if comment and len(comment.strip()) >= 10:
            new_comment = Comment.objects.create(
                owner=request.user,
                project=project,
                body=comment
            )
            new_comment.save()
            return redirect(f'/project/{project.id}#comments-section')

        return self.get(request, *args, **kwargs)


class ProfileView(DetailView):
    model = User
    template_name = 'app_main/profile.html'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['dev_skills'] = self.get_object().skill_set.exclude(description='')
        context['other_skills'] = self.get_object().skill_set.filter(description='')

        return context


def handle_message_submission(request, receiver_id):
    if request.method == 'POST':
        form = MessageForm(request.POST or None, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)

            if request.user.is_authenticated:
                message.sender = request.user
                message.fullname = request.user.fullname
                message.email = request.user.email

            message.receiver = get_object_or_404(User, id=receiver_id)
            message.save()
            return redirect('profile', user_id=receiver_id)

    else:
        form = MessageForm()

    if request.user.is_authenticated:
        form.fields.pop('fullname', None)
        form.fields.pop('email', None)

    context = {
        'form': form,
        'btn_text': 'Send message',
    }

    return render(request, 'form.html', context)


def projects_view(request):
    project_list = Project.objects.all()

    paginator = Paginator(project_list, 3)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)

    context = {
        'projects': projects,
    }
    return render(request, 'app_main/projects.html', context)
