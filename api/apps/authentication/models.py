from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """
    def create_user(self, first_name, last_name, email, contact, password=None):
        """
        Creates and saves a User with the given email, firstname, lastname, contact and password.
        """
        if not email and not first_name and not last_name and not contact:
            raise ValueError(
                'Users must have an email address,first_name, last_name, and contact')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            contact=contact,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, contact, password, email):
        """
        Creates and saves a superuser with the given email, contact and password.
        """
        user = self.create_user(first_name=first_name,
                             last_name=last_name,
                             email=email,
                             password=password,
                             contact=contact,
                             )
        user.is_admin = True
        user.save()
        return user

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of the it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    contact = models.CharField(max_length=17, blank=True)
    is_admin = models.BooleanField(default=False)
    username = None
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact', 'first_name', 'last_name','password']

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email
    
    def get_full_name(self):
        # The user is identified by their first and last name
        return "{0} {0}".format(self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True