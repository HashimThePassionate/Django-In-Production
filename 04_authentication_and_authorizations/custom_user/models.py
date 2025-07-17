from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_no, password=None, **extra_fields):
        if not phone_no:
            raise ValueError('Phone number zaroori hai')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser ko is_staff=True chahiye')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser ko is_superuser=True chahiye')

        return self.create_user(phone_no, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = None
    phone_no = models.CharField('Phone Number', unique=True, max_length=20)
    city = models.CharField('City', max_length=40)

    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['city']         # createsuperuser mein city ka prompt aayega
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_no
