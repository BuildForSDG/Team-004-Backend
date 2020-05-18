from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):

    phone_regex = RegexValidator(regex=r'(\+?\d{1,3})?[-\s]?[6789]\d{9}',
    message = "Phone number entered is invalid")
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    phone_no = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""

        return self.first_name

class SME(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    documents = models.FileField(upload_to='documents/')


class SMEUser(models.Model):
    name = models.CharField(max_length=100)
    sme = models.ForeignKey(SME, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_MODEL_USER, on_delete=models.CASCADE)

class SMEProject(models.Model):
    business_plan = models.TextField()
    tenure = models.DateField()
    documents = models.FileField(upload_to='projects/')
    category = models.CharField(max_length=100)