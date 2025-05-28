from django.db import models
from django.conf import settings

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')

    def fetch_short_bio(self):
        return self.bio[:10]

    def __str__(self):
        return self.name
