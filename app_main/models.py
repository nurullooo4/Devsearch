from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='project-photos/',
                              default='project-photos/project-default.jpg',null=True, blank=True)
    tags = models.ManyToManyField(to='Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source_link = models.URLField(null=True, blank=True)
    demo_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} _ {self.owner.fullname}'

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(to=User, related_name='sent_message', on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(to=User, related_name='receiver_message', on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} - {self.receiver} - {self.body[:50]}'

class Comment(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project,related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner.fullname} - {self.body[:50]}'
