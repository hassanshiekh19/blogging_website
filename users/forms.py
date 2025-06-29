# D:\SCDBlog\blogging_website\users\forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

# -------------------------
# 📅 Registration Form with Profile Fields
# -------------------------
class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=15)
    age = forms.IntegerField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Don't create duplicate Profile — just update the one created by signal
            profile = Profile.objects.get(user=user)
            profile.phone_number = self.cleaned_data['phone_number']
            profile.age = self.cleaned_data['age']
            profile.date_of_birth = self.cleaned_data['date_of_birth']
            profile.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone_number")
        if phone and Profile.objects.filter(phone_number=phone).exists():
            self.add_error("phone_number", "Phone number already exists.")
        return cleaned_data


# -------------------------
# 🔄 Profile Update Form
# -------------------------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'age', 'date_of_birth', 'profile_image']
