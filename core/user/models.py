# Create your models here.
# core/user/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


AUTH_PROVIDER = {
    'email': 'email',
    'facebook': 'facebook',
    'google': 'google',
}


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(
        db_index=True, unique=True,  null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False,
        default=AUTH_PROVIDER.get('email')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"


# Create your models here.
def avatar_dir_path(instance, filename):
    return 'avatar/user_{0}.{1}'.format(instance.base_user.id, 'jpg')


class UserProfile(models.Model):

    GENDER_CHOICES = (
        ('N', 'NotSet'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    base_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default='N')
    avatar = models.FileField(
        upload_to=avatar_dir_path, blank=True, null=True, max_length=200)

    class Meta:
        managed = True
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfile'

    def __str__(self):
        return f"{self.base_user.email}"

    # before saving the instance we’re reducing the image
    def save(self, *args, **kwargs):
        new_image = self.reduce_image_size(self.avatar)
        self.avatar = new_image
        super().save(*args, **kwargs)

    def reduce_image_size(self, avatar):
        img = Image.open(avatar)
        new_size = self.get_new_image_dimensions(img.size, 150)

        if new_size != img.size:
            img = img.resize(new_size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'jpeg', quality=50)
        new_image = File(thumb_io, name=avatar.name)
        return new_image

    def get_new_image_dimensions(self, original_dimensions, new_width):
        original_width, original_height = original_dimensions

        if original_width < new_width:
            return original_dimensions

        aspect_ratio = original_height / original_width

        new_height = round(new_width * aspect_ratio)

        return (new_width, new_height)
