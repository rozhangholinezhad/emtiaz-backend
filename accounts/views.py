from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import UserLoginForm, UserRegistrationForm


@require_http_methods(["GET", "POST"])
def register_view(request):
    """ثبت‌نام کاربر جدید."""
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    form = UserRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "ثبت‌نام با موفقیت انجام شد.")
        return redirect("accounts:profile")

    return render(request, "accounts/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """ورود کاربر با شماره موبایل."""
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    form = UserLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "با موفقیت وارد شدید.")
        next_url = request.GET.get("next") or "accounts:profile"
        return redirect(next_url)

    return render(request, "accounts/login.html", {"form": form})


@require_http_methods(["POST", "GET"])
def logout_view(request):
    """خروج کاربر."""
    logout(request)
    messages.info(request, "از حساب کاربری خارج شدید.")
    return redirect("accounts:login")


@login_required
def profile_view(request):
    """نمایش پروفایل کاربر لاگین‌شده."""
    return render(request, "accounts/profile.html", {"user_obj": request.user})
