from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, profile=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(
            email=self.normalize_email(email),
            profile=profile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, profile=None):
        user = self.create_user(
            email,
            password=password,
            profile=profile,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, profile=None):
        user = self.create_user(
            email,
            password=password,
            profile=profile,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that is built in.

    # Custom Fields
    profile = models.OneToOneField("Profile", on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Profile(models.Model):
    name = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=100, default='', unique=True)
    bio = models.CharField(max_length=240, default='', verbose_name="Biography")
    balance = models.IntegerField(default=0)
    current_challenge = models.OneToOneField("Challenge", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=100, default='')
    participants = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    point_value = models.IntegerField()
    description_text = models.CharField(max_length=1000)
    CHALLENGE_TYPES = (
        ('1', 'Easy'),
        ('2', 'Medium'),
        ('3', 'Pete would be proud'),
    )
    challenge_type = models.CharField(max_length=1, choices=CHALLENGE_TYPES)

    def __str__(self):
        return self.description_text
