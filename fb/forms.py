from django.forms import (
    Form, CharField, Textarea, PasswordInput, ChoiceField, DateField,
    ImageField, TextInput,
)

from fb.models import UserProfile


class UserPostForm(Form):
    text = CharField(widget=Textarea(
        attrs={'rows': 1, 'cols': 40, 'class': 'form-control','placeholder': "What's on your mind?"}))
    photo = ImageField(required = False)    

class UserPostCommentForm(Form):
    text = CharField(widget=Textarea(
        attrs={'rows': 1, 'cols': 50, 'class': 'form-control','placeholder': "Write a comment..."}))

class UserLogin(Form):
    username = CharField(widget=TextInput(attrs={'class': 'form-control username','placeholder': "Your username"}))
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control password','placeholder': "Your Password"}))

class UserProfileForm(Form):
    first_name = CharField(max_length=100, required=False)
    last_name = CharField(max_length=100, required=False)
    gender = ChoiceField(choices=UserProfile.GENDERS, required=False)
    date_of_birth = DateField(required=False)
    avatar = ImageField(required=False)

class UserAlbumForm(Form):
    name = CharField(widget=TextInput(attrs={'class': 'form-control username','placeholder': "Your username"}))
    description = CharField(widget=Textarea(
        attrs={'rows': 3, 'cols': 50, 'class': 'form-control','placeholder': "Describe album..."}))

class PhotosAlbumForm(Form):
    photo = ImageField(required=False)
    photo_description =  CharField(widget=Textarea(
         attrs={'rows': 1, 'cols': 30, 'class': 'form-control','placeholder': "Photo description..."}))
