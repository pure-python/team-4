from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static
from django.conf import settings


class UserPost(models.Model):
    text = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, related_name='posts')
    likers = models.ManyToManyField(User, related_name='liked_posts')
    shares = models.ManyToManyField(User, related_name = 'shared_posts')
    
    photo = models.ImageField(upload_to='images/', blank=False, null=True)
    
    def __unicode__(self):
        return '{} @ {}'.format(self.author, self.date_added)

    class Meta:
        ordering = ['-date_added']

class UserAlbum(models.Model):
    name = models.TextField(max_length=30)
    description = models.TextField()
    user = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{} @ {}'.format(self.user, self.date_added)

    class Meta:
        ordering = ['-date_added']

class AlbumPhoto(models.Model):
    photo_path = models.ImageField(upload_to='albums/', blank=False, null=True)
    album = models.ForeignKey(UserAlbum)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{} @ {}'.format(self.album, self.date_added)

    class Meta:
        ordering = ['-date_added']

class UserPostComment(models.Model):
    text = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User)
    post = models.ForeignKey(UserPost)

    def __unicode__(self):
        return '{} @ {}'.format(self.author, self.date_added)

    class Meta:
        ordering = ['date_added']


class UserProfile(models.Model):
    GENDERS = (
        ('-', 'Unknown'),
        ('F', 'Female'),
        ('M', 'Male'),
    )
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default='-')
    avatar = models.ImageField(upload_to='images/', blank=False, null=True)

    user = models.OneToOneField(User, related_name='profile')

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar \
            else static(settings.AVATAR_DEFAULT)


@receiver(post_save, sender=User)
def callback(sender, instance, *args, **kwargs):
    if not hasattr(instance, 'profile'):
        instance.profile = UserProfile()
        instance.profile.save()
