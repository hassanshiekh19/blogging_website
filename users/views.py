from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import ProfileUpdateForm, CustomUserRegisterForm
from .models import Profile

# -------------------------
# ✅ Register View (with extra fields)

def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = CustomUserRegisterForm()
    return render(request, 'register.html', {'form': form})
# -------------------------
# ✅ Login View
# -------------------------
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# -------------------------
# ✅ Logout View
# -------------------------
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

# -------------------------
# ✅ Profile View + Update
# -------------------------
@login_required
def profile_view(request):
    # Ensure the profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'users/profile.html', {'form': form, 'profile': profile})
