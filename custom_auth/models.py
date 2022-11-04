from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

import re
 
def isValid(s):
     
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    return Pattern.match(s)
 

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            password=password,
            email=self.normalize_email(email),
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=200, blank=False, null=False)

    YEARS = (
        ("ONE", "1st year"),
        ("TWO", "2nd year"),
        ("THREE", "3rd year"),
        ("FOUR", "4th year"),
    )
    year = models.CharField(max_length=20, choices=YEARS, blank=False, null=False)

    # contact no
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="")
    phone_number = models.CharField(validators=[isValid], max_length=15, blank=True, null = True) # Validators should be a list


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return f"{self.email}"

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app?
    def has_module_perms(self, app_label):
        return True
