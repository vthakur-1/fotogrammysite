from django import forms
from allauth.account.forms import SignupForm
from .models import Album, Profile, Photographer, Comment , Photo
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
        profile.save()


class SignupPhotographerForm(SignupCustomerForm, ModelForm):
    class Meta:
        model = Photographer
        fields = ['bio']


class AlbumAddForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'profile']
        widgets = {'profile': forms.HiddenInput()}


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
