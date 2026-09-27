from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get("next") or "analyzer")

    next_url = request.GET.get("next") or request.POST.get("next") or ""

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url or "analyzer")
    else:
        form = AuthenticationForm(request)

    return render(request, "accounts/login.html", {"form": form, "next": next_url})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("analyzer")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(request.POST.get("next") or "analyzer")
    else:
        form = UserCreationForm()

    return render(
        request,
        "accounts/signup.html",
        {
            "form": form,
            "next": request.GET.get("next") or "",
        },
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")
