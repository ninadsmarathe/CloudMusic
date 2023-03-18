from django.contrib.auth import login, get_user_model, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UserCreationForm, UserLoginForm

User = get_user_model()


def registrationForm(request, *args, **kwargs):
    data = ""
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        data = "user is registered"
        return HttpResponseRedirect("/login/")
    # else:
    #     data = "user is not registered...Some error might have occurred!"
    context = {
        "form": form,
        "data": data
    }
    return render(request, "accounts/registration-form.html", context)


def loginForm(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        return HttpResponseRedirect("/albums/")
    return render(request, "accounts/login-form.html", {"form": form})


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect("/login/")
