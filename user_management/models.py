from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    # use_in_migrations = True

    def create_user(self, first_name, last_name, phone_no, email, password, **extra_fields):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError('User must have an email')

        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            email=email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, phone_no, email, password):
        """Creates and saves superuser with given email and password."""
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            email=email,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # TODO: Find out why this validator contains [6789]
    phone_regex = RegexValidator(regex=r'(\+{0,1}\d{1,3})?[-\s]?[6789]\d{9}',
                                 message="Phone number entered is invalid")
    email = models.EmailField(_('Email'), unique=True)
    first_name = models.CharField(
        _('First Name'),
        max_length=225,
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=225,
    )
    date_joined = models.DateTimeField(
        _('Date Joined'),
        auto_now_add=True
    )
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_staff = models.BooleanField(_('Is Staff'), default=False)
    phone_no = models.CharField(
        _('Phone Number'),
        validators=[phone_regex],
        max_length=17,
        blank=True
    )

    USER_ROLE_CHOICES = (
        ("SME_USER", "SME_USER"),
        ("INVESTOR_USER", "INVESTOR_USER"),
        ("BACKOFFICE_USER", "BACKOFFICE_USER")
    )
    role = models.CharField(
        max_length=225,
        choices=USER_ROLE_CHOICES,
        default="BACKOFFICE_USER"
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
