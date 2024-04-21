from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email,first_name,last_name,password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,first_name = first_name,last_name =last_name ,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name, password=None,  **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email,first_name,last_name,password,  **extra_fields)

class CustomUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [first_name,last_name]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        
        if not self.first_name:
            raise ValueError("The 'first_name' field must be set")
        if not self.last_name:
            raise ValueError("The 'last_name' field must be set")
        super().save(*args, **kwargs)



class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='friend_requests_received', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

class Friendship(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='friendships_1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='friendships_2', on_delete=models.CASCADE)
