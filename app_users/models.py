from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import MyUserManager as UserManager

class User(AbstractUser):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    username = models.CharField(max_length=100, verbose_name="Username",
                                null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    bio = models.TextField(verbose_name="About", null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile-images/", verbose_name="Profile Image",
                                      default="profile-images/user-default.jpg",
                                      null=True, blank=True)
    location = models.CharField(max_length=200, verbose_name="Basin in", null=True, blank=True)
    occupation = models.CharField(max_length=200, verbose_name="Occupation", null=True, blank=True)
    social_telegram = models.URLField(verbose_name="Telegram", max_length=200, null=True, blank=True)
    social_instagram = models.URLField(verbose_name="Instagram", max_length =200, null=True, blank=True)
    social_facebook = models.URLField(verbose_name="Facebook", max_length =200, null=True, blank=True)
    social_twitter = models.URLField(verbose_name="Twitter", max_length =200, null=True, blank=True)
    social_whatsapp = models.URLField(verbose_name="Whatsapp", max_length =200, null=True, blank=True)
    social_linkedin = models.URLField(verbose_name="LinkedIn", max_length =200, null=True, blank=True)
    social_youtube = models.URLField(verbose_name="YouTube", max_length =200, null=True, blank=True)
    social_github = models.URLField(verbose_name="GitHub", max_length =200, null=True, blank=True)
    social_website = models.URLField(verbose_name="Website", max_length =200, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def set_fullname(self, value):
        names = value.split()
        self.first_name, self.last_name = names[0], " ".join(names[1:])

    fullname = property(get_fullname, set_fullname)

class Skill(models.Model):
    owner = models.ForeignKey(to=User,  on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.owner}-{self.name}'
