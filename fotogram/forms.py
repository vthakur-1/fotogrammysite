from django import forms
from allauth.account.forms import SignupForm
from guardian.shortcuts import assign_perm
from .models import Album, Profile, Photographer, Comment, Photo
from django.contrib.auth.models import Group

from django.forms import ModelForm

from django.contrib.auth.models import User


class SignupCustomerForm(SignupForm, ModelForm):
    first_name = forms.CharField(max_length=100)

    class Meta:
        model = Profile
        fields = ['image', 'username', 'email']

    def save(self, request):
        # import pdb;pdb.set_trace()
        profile = super(SignupCustomerForm, self).save(request)
        profile.first_name = self.cleaned_data['first_name']
        profile.image = self.cleaned_data['image']
        profile.is_customer = True
        profile.username = self.cleaned_data['username']
        profile.email = self.cleaned_data['email']
        group = Group.objects.get(name="customer")
        group.user_set.add(profile)
        profile.save()
        return profile


class SignupPhotographerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupPhotographerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Photographer
        fields = ['bio']

    def save(self, *args, **kwargs):
        self.instance.profile = kwargs.pop('profile', None)
        self.instance.bio = self.cleaned_data['bio']
        group = Group.objects.get(name="photographer")
        group.user_set.add(self.instance.profile)
        super(SignupPhotographerForm, self).save(*args, **kwargs)
        self.instance.profile.is_photographer = True
        self.instance.profile.is_customer = False
        self.instance.profile.save()


class AlbumAddForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'profile']
        widgets = {'profile': forms.HiddenInput()}

    def save(self, request):
        user = Profile.objects.get(pk=request.user.id)
        album = super(AlbumAddForm, self).save(request)
        album.name = self.cleaned_data['name']
        # import pdb;pdb.set_trace()
        assign_perm('delete_album', user, album)
        album.save()
        return album


class AlbumAddPhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'album', 'image', 'tag']
        widgets = {'album': forms.HiddenInput()}



class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'photo', 'profile']
        widgets = {'photo': forms.HiddenInput(), 'profile': forms.HiddenInput()}
