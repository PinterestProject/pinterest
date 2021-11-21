from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
from django.contrib.auth import get_user_model
from Categories.models import Category


class UserManager(BaseUserManager):
    """
    this class created to handle user model operation like create user or super user
    which inherit form BaseUserManager like user class inherit from AbstractBaseUser to
    implement the some required function
    """
    def create_user(self,name,email,password=None):
        """
        create new user with no super rights
        normalize_email : used to make all mails in one lower case format
        set_password : to store password as hashed not plain text
        """
        if not email:
            raise ValueError('user must have email address')
        email=self.normalize_email(email)
        user=self.model(email=email,name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,name,email,password=None):
        """
        from this function you'll able to create user with super rights
        :param name: str
        :param email: str
        :param password: str
        :return: user object

        """
        user=self.create_user(name,email,password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=225,unique=True)
    birth_day = models.DateField(null=True)
    gender = models.TextField(choices=[
        ('male', 'Male'),
        ('female','Female')
    ],null=True)
    pronoun = models.TextField(choices=[
        ('he', 'He'),
        ('she','She')
    ],null=True)
    language = models.TextField(choices=[
        ('arabic', 'ar'),
        ('english','en')
    ],null=True)

    address = models.CharField(max_length=225,null=True)
    bio = models.TextField(max_length=3000,null=True)
    profile_image=models.ImageField(upload_to='User/profile',null=True)
    cover_image=models.ImageField(upload_to='User/cover',null=True)
    social_facebook=models.CharField(max_length=100,null=True)
    social_google=models.CharField(max_length=100,null=True)
    social_twitter=models.CharField(max_length=100,null=True)
    history=models.JSONField(null=True,default={'recent_categories':[]})
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category)
    following = models.ManyToManyField('self', through='Relationship', related_name='followers', symmetrical=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name']

    objects=UserManager()
    def __str__(self):

        return self.email

class Relationship(models.Model):
    follower_id = models.ForeignKey("User",on_delete=models.CASCADE,related_name='rel_from_set')
    followed_id = models.ForeignKey("User",on_delete=models.CASCADE, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.follower_id,self.followed_id)
