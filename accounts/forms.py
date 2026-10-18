from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class UserRegistrationForm(forms.ModelForm):
    """فرم ثبت‌نام با شماره موبایل."""

    password1 = forms.CharField(
        label="رمز عبور",
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm",
                "placeholder": "حداقل ۸ کاراکتر",
                "autocomplete": "new-password",
            }
        ),
        help_text="حداقل ۸ کاراکتر.",
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm",
                "placeholder": "تکرار رمز عبور",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("phone", "first_name", "last_name")
        labels = {
            "phone": "شماره موبایل",
            "first_name": "نام",
            "last_name": "نام خانوادگی",
        }
        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm",
                    "placeholder": "09123456789",
                    "dir": "ltr",
                    "inputmode": "numeric",
                    "autocomplete": "tel",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm",
                    "placeholder": "نام",
                    "autocomplete": "given-name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm",
                    "placeholder": "نام خانوادگی",
                    "autocomplete": "family-name",
                }
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        phone = User.objects.normalize_phone(phone)
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("این شماره موبایل قبلاً ثبت شده است.")
        return phone

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "رمز عبور و تکرار آن یکسان نیستند.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """فرم ورود با شماره موبایل (فیلد username = phone)."""

    username = forms.CharField(
        label="شماره موبایل",
        widget=forms.TextInput(
            attrs={
                "class": "field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm",
                "placeholder": "09123456789",
                "dir": "ltr",
                "inputmode": "numeric",
                "autocomplete": "username",
            }
        ),
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "field-input w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-sm tracking-wider",
                "placeholder": "رمز عبور خود را وارد کنید",
                "autocomplete": "current-password",
            }
        ),
    )

    error_messages = {
        "invalid_login": "شماره موبایل یا رمز عبور اشتباه است.",
        "inactive": "این حساب کاربری غیرفعال است.",
    }

    def clean_username(self):
        phone = self.cleaned_data.get("username", "")
        return User.objects.normalize_phone(phone)
