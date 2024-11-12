from django.forms import ModelForm

from .models import Project, Message

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'image', 'source_link', 'demo_link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input input--text',
            })

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['fullname', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})
        if user and user.is_authenticated:
            self.fields['fullname'].required = False
            self.fields['email'].required = False

