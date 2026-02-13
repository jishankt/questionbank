from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, ProfileForm
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():

            # ⭐ Save user safely (handles password hashing)
            user = form.save()

            # ⭐ Save profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('login')

    else:
        form = RegisterForm()
        profile_form = ProfileForm()

    return render(request, 'register.html', {
        'form': form,
        'profile_form': profile_form
    })

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_staff:
                return redirect('uploader_dashboard')

            return redirect('paper_list')

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

