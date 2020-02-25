
from django.contrib.auth.models import AbstractUser
from django.db import models


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(TimeStamp, AbstractUser):
    is_customer = models.BooleanField('customer status', default=False)
    is_photographer = models.BooleanField('photographer status', default=False)
    image = models.ImageField()

    # def __str__(self):
    #     return self.user.username


class Photographer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=300)


class Album(TimeStamp):
    profile = models.ForeignKey( Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Photo(TimeStamp):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default="")
    tag = models.ManyToManyField(Tag)
    title = models.CharField(max_length=40)
    image = models.ImageField(upload_to='photos')
    like_count = models.IntegerField(null='true')
    description = models.TextField(max_length=400, null=True)

    def __str__(self):
        return self.title


#
class Comment(TimeStamp):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.CharField(max_length=400)

    # def __str__(self):
    #     return self.profile.user.username


class Like(TimeStamp):
    class Meta:
        unique_together = (('photo', 'profile'),)

    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.photo
