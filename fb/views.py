from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden

from fb.models import UserPost, UserPostComment, UserProfile, UserAlbum, AlbumPhoto
from fb.forms import (
    UserPostForm, UserPostCommentForm, UserLogin, UserProfileForm,
    UserAlbumForm, PhotosAlbumForm
)


@login_required
def index(request):
    posts = UserPost.objects.all()
    if request.method == 'GET':
        form = UserPostForm()

    elif request.method == 'POST':
        form = UserPostForm(request.POST, request.FILES)
        if form.is_valid():           
            text = form.cleaned_data['text']

            if form.cleaned_data['photo']:
                photo = form.cleaned_data['photo']
                post = UserPost(text=text, author=request.user, photo=photo)

            else:
                post = UserPost(text=text, author=request.user)

            post.save()

    context = {
        'posts': posts,
        'form': form,
    }

    return render(request, 'index.html', context)


@login_required
def post_details(request, pk):
    post = UserPost.objects.get(pk=pk)

    if request.method == 'GET':
        form = UserPostCommentForm()
    elif request.method == 'POST':
        form = UserPostCommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            comment = UserPostComment(text=cleaned_data['text'],
                                      post=post,
                                      author=request.user)
            comment.save()

    comments = UserPostComment.objects.filter(post=post)

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'post_details.html', context)

@login_required
def user_album(request, user):
    albums = UserAlbum.objects.filter(user__username = user)
    if request.method == 'GET':
        form = UserAlbumForm()
    elif request.method == 'POST':
        form = UserAlbumForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data;
            album = UserAlbum(name=cleaned_data['name'], description=cleaned_data['description'],
                              user=request.user )
            album.save()
            # if form.cleaned_data['photo']:
            #     photo = AlbumPhoto(photo_path=cleaned_data['photo'], album=album, 
            #         description=cleaned_data['photo_description']
            return redirect('/profile/' + user + '/albums/' + str(album.id) )
    context = {
        'form': form,
        'albums': albums,
    }

    return render(request, 'albums.html', context)

@login_required
def user_album_photos(request, user, pk):
    album = UserAlbum.objects.get(pk = pk)
    photos = AlbumPhoto.objects.filter(album__id=album.id)
    if request.method == 'GET':
        form = PhotosAlbumForm()
    elif request.method == 'POST':
        form = PhotosAlbumForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            image = AlbumPhoto( photo_path = form.cleaned_data['photo'],
                                description=form.cleaned_data['photo_description'], album = album )
            
            image.save()
            form = PhotosAlbumForm()

    context = {
        'form' : form,
        'album' : album,
        'photos' : photos,
    }

    return render(request, 'album_photos.html', context)

def login_view(request):
    if request.method == 'GET':
        login_form = UserLogin()
        context = {
            'form': login_form,
        }
        return render(request, 'login.html', context)

    if request.method == 'POST':
        login_form = UserLogin(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {
                'form': login_form,
                'message': 'Wrong user and/or password!',
            }
            return render(request, 'login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def profile_view(request, user):
    profile = UserProfile.objects.get(user__username=user)
    post_share = UserPost.objects.filter(shares__username = user)

    albums = UserAlbum.objects.filter(user__username=user)
    photos = {}
    for album in albums:
        aux = AlbumPhoto.objects.filter(album__id = album.id).last()     
        photos[album.id] = aux

    context = {
        'profile': profile,
        'photos' : photos,
        'albums' : albums,
        'post_share': post_share,
    }
    
    return render(request, 'profile.html', context)


@login_required
def edit_profile_view(request, user):
    profile = UserProfile.objects.get(user__username=user)
    if not request.user == profile.user:
        return HttpResponseForbidden()
    if request.method == 'GET':
        data = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'gender': profile.gender,
            'date_of_birth': profile.date_of_birth,
        }
        avatar = SimpleUploadedFile(
            profile.avatar.name, profile.avatar.file.read()) \
            if profile.avatar else None
        file_data = {'avatar': avatar}
        form = UserProfileForm(data, file_data)
    elif request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.user.save()

            profile.gender = form.cleaned_data['gender']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            
            if form.cleaned_data['avatar']:
                profile.avatar = form.cleaned_data['avatar']
            profile.save()

            return redirect(reverse('profile', args=[profile.user.username]))
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)


@login_required
def like_view(request, pk):
    post = UserPost.objects.get(pk=pk)
    post.likers.add(request.user)
    post.save()
    return redirect(reverse('post_details', args=[post.pk]))

@login_required
def like_view_index(request, pk):
    post = UserPost.objects.get(pk=pk)
    post.likers.add(request.user)
    post.save()
    return redirect(reverse('index'))

@login_required
def share_view(request, pk):
    post = UserPost.objects.get(pk=pk)
    post.shares.add(request.user)
    post.save()
    return redirect(reverse('post_details', args=[post.pk]))

@login_required
def share_view_index(request, pk):
    post = UserPost.objects.get(pk=pk)
    post.shares.add(request.user)
    post.save()
    return redirect(reverse('index'))
