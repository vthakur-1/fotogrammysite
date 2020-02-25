from django.shortcuts import render
from fotogram.models import Profile, Comment, Photo, Like
from fotogram.forms import SignupCustomerForm, SignupPhotographerForm, AddCommentForm, AlbumAddPhotoForm, AlbumAddForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
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
            return HttpResponseRedirect(reverse('dashboard'))

    form = SignupCustomerForm()
    return render(request, 'ds.html', {'form': form})


def photographersignup(request):
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        form = SignupPhotographerForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('profile'))
    else:
        form =  SignupPhotographerForm()
        return render(request, 'ds.html', {'form': form})


def dashboard(request):
    photo = Photo.objects.all()
    # import pdb;pdb.set_trace()
    if 'search' in request.GET:
        search_term = request.GET['search']
        photo = Photo.objects.filter(Q(title__icontains=search_term) | Q(album__name__icontains=search_term) |
                                     Q(tag__name__icontains=search_term))
    # import pdb;pdb.set_trace()

    return render(request, 'dashboard.html', {'photo': photo})


def addalbum(request):
    if request.method == 'POST':
        form = AlbumAddForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('profile'))
    else:
        form = AlbumAddForm(initial={'profile': request.user.profile.id})
        return render(request, 'create.html', {'form': form})


def addphoto(request, album_id):
    if request.method == 'POST':
        form = AlbumAddPhotoForm(request.POST, request.FILES, initial={'tag': request.POST['tag']})
        form.save()
        return HttpResponseRedirect(reverse('profile'))
    form = AlbumAddPhotoForm(initial={'album': album_id})
    return render(request, 'ds.html', {'form': form})


def viewphoto(request, photo_id):
    photos = Photo.objects.get(id=photo_id)
    comments = Comment.objects.filter(photo_id=photo_id)
    form = AddCommentForm()
    context = {'photos': photos, 'form': form, 'comments': comments}
    return render(request, 'viewphotos.html', context)


def addcomment(request, photo_id, ):
    if request.method == 'POST':
        photo = get_object_or_404(Photo, id=photo_id)
        profile = get_object_or_404(Profile, id=request.user.profile.id)
        comment = Comment(photo=photo, profile=profile, comment=request.POST['comment'])
        comment.save()
        return HttpResponseRedirect(reverse('profile'))
    form = AddCommentForm()
    return render(request, 'viewphotos.html', {'form': form})


def viewcomment(request, photo_id, album_id):
    comment = Comment.objects.filter(photo_id=photo_id)
    return render(request, 'viewcomments.html', {'comment': comment})


def addlike(request, photo_id, album_id):
    try:
        photo = get_object_or_404(Photo, id=photo_id)
        like = Like(photo=photo, profile=request.user.profile)
        like.save()
        return HttpResponseRedirect(reverse('profile'))
    except IntegrityError:
        return HttpResponse("Exception: you already like this")
