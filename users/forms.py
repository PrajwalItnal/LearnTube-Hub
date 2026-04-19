from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Courses

class CustomSignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('publisher', 'Publisher'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        widget=forms.RadioSelect,
        required=True
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) <= 5:
            raise forms.ValidationError("Username must be greater than 5 characters long.")
        if not all(c.isalpha() or c == '_' for c in username):
            raise forms.ValidationError("Username can only contain letters and underscores (numbers are not allowed).")
        return username

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Tell us about yourself...', 'class': 'form-control', 'rows': 3}),
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role' , 'bio')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['title', 'description', 'video_url']
        widgets = {
            'title' : forms.TextInput(attrs = {'class' : 'form-control', 'placeholder' : 'Course title'}),
            'description' : forms.Textarea(attrs = {'class' : 'form-control', 'placeholder' : 'Course description'}),
            'video_url' : forms.URLInput(attrs = {'class' : 'form-control', 'placeholder' : 'YouTube video link'})
        }

    def clean_video_url(self):
        video_url = self.cleaned_data.get('video_url')
        regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
        
        if video_url:
            match = re.search(regex, video_url)
            if not match:
                raise forms.ValidationError("Please provide a valid YouTube video link (e.g., https://www.youtube.com/watch?v=...)")
        
        return video_url
