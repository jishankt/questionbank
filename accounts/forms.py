from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile


# ---------------- USER REGISTER FORM ----------------

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ---------------- PROFILE FORM ----------------

class ProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ['class_name', 'school_name']

        widgets = {
            'class_name': forms.Select(attrs={'class': 'dropdown'}),
            'school_name': forms.TextInput(attrs={
                'placeholder': 'Enter School Name'
            })
        }

    # ⭐ Add "Select Class" placeholder
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_name'].empty_label = "Select Class"
