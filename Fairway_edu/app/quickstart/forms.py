from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import inlineformset_factory
from .models import *

class ConsultantSignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio','rows': 3}),
        required=False
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = Consultant
        fields = ('username', 'email', 'bio', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.bio = self.cleaned_data.get('bio', '')  # Use get to handle optional bio
        if commit:
            user.save()
        return user

class ConsultantLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class FolderForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Folder Name'})
        )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control','placeholder': 'Folder Description','rows': 3})
        )
    
    class Meta:
        model = Folder
        fields = ['name', 'description']

# class PictureForm(forms.ModelForm):
#     folder = forms.ModelChoiceField(queryset=Folder.objects.all(), widget=forms.Select(
#             attrs={'class': 'form-control','placeholder': 'Select Folder'})
#     )
#     title = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'class': 'form-control','placeholder': 'Picture Title'})
#     )
#     image = forms.ImageField(
#         widget=forms.ClearableFileInput(
#             attrs={'class': 'form-control','accept': 'image/*'})
#     )
#     description = forms.CharField(
#         widget=forms.Textarea(
#             attrs={'class': 'form-control','placeholder': 'Picture Description','rows': 3})
#     )
    
#     class Meta:
#         model = Picture
#         fields = ['folder', 'title', 'image', 'description']
class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['folder', 'title', 'image', 'description']
        widgets = {
            'folder': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Picture Title'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Picture Description', 'rows': 3}),
        }

PictureFormSet = inlineformset_factory(
    Folder,
    Picture,
    form=PictureForm,
    extra=9,
    can_delete=True,
)

class ServiceForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Title'})
        )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control','placeholder': 'Description','rows': 3})
        )
    
    class Meta:
        model = Services
        fields = ['title', 'description']