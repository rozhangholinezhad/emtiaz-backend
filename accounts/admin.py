from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """پنل مدیریت کاربران با برچسب‌های فارسی."""

    ordering = ("-date_joined",)
    list_display = (
        "phone",
        "first_name",
        "last_name",
        "is_employee",
        "is_staff",
        "is_active",
        "can_publish_article",
        "can_manage_property",
        "date_joined",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_employee",
        "can_publish_article",
        "can_manage_property",
    )
    search_fields = ("phone", "first_name", "last_name")
    readonly_fields = ("date_joined", "updated_at", "last_login")

    fieldsets = (
        (
            "اطلاعات ورود",
            {"fields": ("phone", "password")},
        ),
        (
            "اطلاعات شخصی",
            {"fields": ("first_name", "last_name")},
        ),
        (
            "وضعیت و نقش",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_employee",
                )
            },
        ),
        (
            "سطوح دسترسی دامنه",
            {
                "fields": (
                    "can_publish_article",
                    "can_manage_property",
                ),
                "description": "مجوزهای اختصاصی برای انتشار مقاله و مدیریت ملک.",
            },
        ),
        (
            "مجوزهای سیستم",
            {
                "fields": ("groups", "user_permissions"),
                "classes": ("collapse",),
            },
        ),
        (
            "تاریخ‌ها",
            {"fields": ("last_login", "date_joined", "updated_at")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_employee",
                    "can_publish_article",
                    "can_manage_property",
                ),
            },
        ),
    )

    filter_horizontal = ("groups", "user_permissions")
