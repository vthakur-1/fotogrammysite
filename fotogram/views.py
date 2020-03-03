from django.shortcuts import render
from fotogram.models import Profile, Comment, Photo, Like, Photographer , Album
from fotogram.forms import SignupCustomerForm, SignupPhotographerForm, AddCommentForm, AlbumAddPhotoForm, AlbumAddForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.db import IntegrityError
from django.contrib.auth.models import Group

from django.contrib.auth.models import User
# from demo_form.forms import *
# from demo_form.models import Author, Book
from django.urls import reverse


def type(request):
    # import pdb;pdb.set_trace()
    return render(request, 'index.html')


def customersignup(request):
    if request.method == 'POST':
        form = SignupCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            profile = Profile.objects.get(username=form['username'].data)
            profile.save()
            return HttpResponseRedirect(reverse('dashboard'))

    form = SignupCustomerForm()
    return render(request, 'ds.html', {'form': form})


def photographersignup(request):

    if request.method == 'POST':
        form2 = SignupCustomerForm(request.POST, request.FILES, prefix="profile")
        # import pdb;
        # pdb.set_trace()
        if form2.is_valid():
            profile = form2.save(request)
            form1 = SignupPhotographerForm(request.POST, prefix="photographer")
            if form1.is_valid():
                form1.save(profile=profile)
                return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        photographer_form = SignupPhotographerForm(prefix="photographer")
        photographer_profile_form = SignupCustomerForm(prefix="profile")
        return render(request, 'ds.html', {'form1': photographer_form, 'form2': photographer_profile_form})


def dashboard(request):
    photo = Photo.objects.all()
    # import pdb;pdb.set_trace()
    if 'search' in request.GET:
        search_term = request.GET['search']
        photo = Photo.objects.filter(Q(title__icontains=search_term) | Q(album__name__icontains=search_term) |
                                     Q(tag__name__icontains=search_term))
    # import pdb;pdb.set_trace()

    return render(request, 'dashboard.html', {'photo': photo})


@login_required()
@permission_required('fotogram.add_album', raise_exception=True)
def addalbum(request):
    if request.method == 'POST':
        form = AlbumAddForm(request.POST)
        form.save(request)
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = AlbumAddForm(initial={'profile': request.user.id})
        return render(request, 'create.html', {'form': form})


@login_required()
@permission_required('fotogram.add_photo', raise_exception=True)
def addphoto(request, album_id):
    if request.method == 'POST':
        album = Album.objects.get(pk=album_id)
        # import pdb;pdb.set_trace()
        # request.user.has_perm('add_photo', album):
        form = AlbumAddPhotoForm(request.POST, request.FILES, initial={'tag': request.POST['tag']})
        form.save()
        return HttpResponseRedirect(reverse('dashboard'))
        # else:
        #     return HttpResponse("Exception: you didn't have access to add photo")
    form = AlbumAddPhotoForm(initial={'album': album_id})
    return render(request, 'addphoto.html', {'form': form})


def viewphoto(request, photo_id):
    photos = Photo.objects.get(id=photo_id)
    comments = Comment.objects.filter(photo_id=photo_id)
    form = AddCommentForm()
    context = {'photos': photos, 'form': form, 'comments': comments}
    return render(request, 'viewphotos.html', context)

@login_required()
def addcomment(request, photo_id, ):
    if request.method == 'POST':
        photo = get_object_or_404(Photo, id=photo_id)
        profile = get_object_or_404(Profile, id=request.user.id)
        comment = Comment(photo=photo, profile=profile, comment=request.POST['comment'])
        comment.save()
        return HttpResponseRedirect(reverse('dashboard'))
    form = AddCommentForm()
    return render(request, 'viewphotos.html', {'form': form})


def viewcomment(request, photo_id, album_id):
    comment = Comment.objects.filter(photo_id=photo_id)
    return render(request, 'viewcomments.html', {'comment': comment})


def addlike(request, photo_id, album_id):
    try:
        photo = get_object_or_404(Photo, id=photo_id)
        like = Like(photo=photo, profile=request.user)
        like.save()
        return HttpResponseRedirect(reverse('dashboard'))
    except IntegrityError:
        return HttpResponse("Exception: you already like this")

@login_required()
@permission_required('fotogram.add_album', raise_exception=True)
def deletealbum(request, album_id):
    album=Album.objects.get(pk=album_id)
    # import pdb;pdb.set_trace()
    if request.user.has_perm('delete_album', album):
        instance1 = Album.objects.get(id=album_id)
        instance1.delete()
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return HttpResponse("Exception: you didn't have permission")
