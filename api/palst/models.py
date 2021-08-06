from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from .core.models import (
    TimeStampModel,
    TaskModel
)
import os, uuid



class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('ユーザーネームは必須項目です。')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class mUser(AbstractBaseUser,
            PermissionsMixin,
            TimeStampModel):

    auth0_id = models.CharField(_('Auth0Id'), max_length=255, unique=True)
    auth0_name = models.CharField(_('Auth0Name'), max_length=255, unique=False)
    username = models.CharField(_('Username'), max_length=70, unique=True, blank=True, null=True)
    email = models.EmailField(_('Email'), max_length=70, unique=True)
    address = models.CharField(_('Address'), max_length=100, blank=True, null=True)

    deleted = models.BooleanField(
        _('Delete Flag'),
        default=False,
        help_text=_(
            'Designates whether the user was deleted or not'
        )
    )

    is_staff = models.BooleanField(
        _('Staff Status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    is_active = models.BooleanField(
        _('Active Flag'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        name = self.auth0_name if self.auth0_name != '' else self.username
        return name

    def get_username(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Stock(models.Model):

    # jupyterでDataframeからそのまま入れたいためリレーションつけない
    code = models.PositiveSmallIntegerField()
    open = models.DecimalField(
        max_digits=20,
        decimal_places=10
    )
    close = models.DecimalField(
        max_digits=20,
        decimal_places=10
    )
    high = models.DecimalField(
        max_digits=20,
        decimal_places=10
    )
    low = models.DecimalField(
        max_digits=20,
        decimal_places=10
    )
    volume = models.DecimalField(
        max_digits=20,
        decimal_places=10
    )
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.code)


class Company(models.Model):

    # とりあえず今は2項目のみ必須。後で色々情報入れたい
    code = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=255)

    # address = models.CharField(max_length=255, null=True, blank=True)
    # yearBorn = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
