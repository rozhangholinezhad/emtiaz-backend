from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import UserLoginForm, UserRegistrationForm


@require_http_methods(["GET", "POST"])
def register_view(request):
    """ثبت‌نام کاربر جدید با شماره موبایل."""
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
    """ورود با شماره موبایل و پشتیبانی از «مرا به خاطر بسپار»."""
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    form = UserLoginForm(request, data=request.POST or None)
    next_url = request.POST.get("next") or request.GET.get("next") or ""

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        if request.POST.get("remember"):
            # ۲ هفته
            request.session.set_expiry(60 * 60 * 24 * 14)
        else:
            request.session.set_expiry(0)

        messages.success(request, "با موفقیت وارد شدید.")
        if next_url:
            return redirect(next_url)
        return redirect("accounts:profile")

    return render(
        request,
        "accounts/login.html",
        {"form": form, "next": next_url},
    )


@require_http_methods(["POST", "GET"])
def logout_view(request):
    """خروج از حساب."""
    logout(request)
    messages.info(request, "از حساب کاربری خارج شدید.")
    return redirect("accounts:login")


@login_required
def profile_view(request):
    """پروفایل کاربر لاگین‌شده."""
    return render(request, "accounts/profile.html", {"user_obj": request.user})
