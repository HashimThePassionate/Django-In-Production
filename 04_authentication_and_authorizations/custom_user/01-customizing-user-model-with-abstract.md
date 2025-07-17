# 📱 **Custom Django User Model with Phone-Number Authentication**

A step-by-step guide for extending Django's default user model to use `phone_no` instead of `username`, adding a custom `city` field, and integrating seamlessly with Django's admin panel.

---

## 🗂 **Table of Contents**

- [📱 **Custom Django User Model with Phone-Number Authentication**](#-custom-django-user-model-with-phone-number-authentication)
  - [🗂 **Table of Contents**](#-table-of-contents)
  - [🛠 **Prerequisites**](#-prerequisites)
  - [🎯 **Create the `custom_user` App**](#-create-the-custom_user-app)
  - [🚧 **Define a Custom User Model**](#-define-a-custom-user-model)
    - [📌 **Imports**](#-imports)
    - [🔐 **Custom User Manager**](#-custom-user-manager)
    - [🧑‍💻 **Custom User Model**](#-custom-user-model)
  - [⚙️ **Configure Django Settings**](#️-configure-django-settings)
  - [🖥️ **Customize the Admin Interface**](#️-customize-the-admin-interface)
    - [📝 **Admin Forms**](#-admin-forms)
    - [📋 **Admin Registration**](#-admin-registration)
  - [🚀 **Apply Migrations \& Create Superuser**](#-apply-migrations--create-superuser)
  - [📖 **How It Works**](#-how-it-works)

---

## 🛠 **Prerequisites**

Ensure you have:

* Python ≥ 3.8
* Django ≥ 3.2
* An existing Django project configured with a database.

---

## 🎯 **Create the `custom_user` App**

```bash
python manage.py startapp custom_user
```

This generates a new app `custom_user` to centralize your user model logic in `custom_user/models.py`.

---

## 🚧 **Define a Custom User Model**

### 📌 **Imports**

```python
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
```

* `BaseUserManager`: To customize user creation.
* `AbstractUser`: A ready-to-use extendable base user model.
* `models`: To define database fields.

### 🔐 **Custom User Manager**

```python
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_no, password=None, **extra_fields):
        if not phone_no:
            raise ValueError('Phone number is required')
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
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(phone_no, password, **extra_fields)
```

This manager ensures proper creation and validation of users and superusers.

### 🧑‍💻 **Custom User Model**

```python
class CustomUser(AbstractUser):
    username = None
    email = None
    phone_no = models.CharField('Phone Number', unique=True, max_length=20)
    city = models.CharField('City', max_length=40)

    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['city']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_no
```

* Removes default username/email fields.
* Introduces `phone_no` as a unique identifier and a `city` field.
* Makes `phone_no` the primary authentication identifier.

---

## ⚙️ **Configure Django Settings**

Update your `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps ...
    'custom_user',
    # ... other apps ...
]

AUTH_USER_MODEL = 'custom_user.CustomUser'
```

Registers your custom user model globally in Django.

---

## 🖥️ **Customize the Admin Interface**

### 📝 **Admin Forms**

Create custom forms for admin integration:

```python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone_no', 'city')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone_no', 'city', 'is_active', 'is_staff')
```

Ensures admin forms reflect the new user fields.

### 📋 **Admin Registration**

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('phone_no', 'city', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('phone_no',)
    ordering = ('phone_no',)

    fieldsets = (
        (None, {'fields': ('phone_no', 'password')}),
        ('Personal Info', {'fields': ('city',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_no', 'city', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
```

Registers the custom user model with a tailored admin UI.

---

## 🚀 **Apply Migrations & Create Superuser**

Run the following commands:

```bash
python manage.py makemigrations custom_user
python manage.py migrate
python manage.py createsuperuser
```

Sets up database and superuser access using your custom model.

---

## 📖 **How It Works**

* Extends `AbstractUser` for built-in security.
* Uses `phone_no` as the primary identifier (`USERNAME_FIELD`).
* Implements a custom manager for secure, consistent user creation.
* Customizes Django admin forms and views for seamless integration.
* Globally configures Django to use the `CustomUser` model.

