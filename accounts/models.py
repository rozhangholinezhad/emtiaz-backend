from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from .managers import UserManager


phone_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="شماره موبایل باید ۱۱ رقم و با ۰۹ شروع شود (مثال: ۰۹۱۲۳۴۵۶۷۸۹).",
)


class User(AbstractBaseUser, PermissionsMixin):
    """
    مدل کاربر سفارشی بر پایه شماره موبایل.

    سطح دسترسی‌های can_publish_article و can_manage_property
    برای کنترل آیندهٔ انتشار مقاله و افزودن ملک در نظر گرفته شده‌اند.
    """

    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[phone_validator],
        verbose_name="شماره موبایل",
        help_text="شماره موبایل ۱۱ رقمی با فرمت ۰۹xxxxxxxxx",
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="نام",
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="نام خانوادگی",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
        help_text="کاربر غیرفعال نمی‌تواند وارد سیستم شود.",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="دسترسی به پنل ادمین",
        help_text="تعیین می‌کند کاربر بتواند وارد پنل مدیریت Django شود.",
    )
    is_employee = models.BooleanField(
        default=False,
        verbose_name="کارمند",
        help_text="آیا این کاربر کارمند مجموعه است؟",
    )

    # سطوح دسترسی دامنه برای آینده
    can_publish_article = models.BooleanField(
        default=False,
        verbose_name="مجوز انتشار مقاله",
        help_text="اجازهٔ ایجاد و انتشار مقاله در بخش وبلاگ.",
    )
    can_manage_property = models.BooleanField(
        default=False,
        verbose_name="مجوز مدیریت ملک",
        help_text="اجازهٔ افزودن، ویرایش و مدیریت املاک.",
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ عضویت",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین به‌روزرسانی",
    )

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-date_joined"]

    def __str__(self):
        full = self.get_full_name()
        return full if full else self.phone

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name or self.phone
