from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
 
# we extends user model when we want to add column very related to authentication
# it's hard to extend the user model in the middle of the project because we had already users and migrations dependent on the default user model
# best practice is to create custom user model at the start of every project even we make it empty
class User(AbstractUser):
    email = models.EmailField(unique=True)    