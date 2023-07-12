from django.shortcuts import render, redirect
from .forms import AuthForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def login_user(request):
    redirect_to = 'core:index'
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, "You are now logged in!")
                    return redirect(redirect_to)
    return render(request, 'registration/login.html')

def logout_user(request):
    if request.user.is_authenticated:
        messages.success(request, "You have been logged out.")
        logout(request)
        return redirect("core:index")
    messages.error(request, "You are already logged out.")
    return redirect("core:index")
