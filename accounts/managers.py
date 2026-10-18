from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """مدیر ساخت کاربر با شماره موبایل به‌عنوان شناسه اصلی."""

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("شماره موبایل الزامی است.")
        phone = self.normalize_phone(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_employee", True)
        extra_fields.setdefault("can_publish_article", True)
        extra_fields.setdefault("can_manage_property", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("سوپریوزر باید is_staff=True داشته باشد.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("سوپریوزر باید is_superuser=True داشته باشد.")

        return self.create_user(phone, password, **extra_fields)

    @staticmethod
    def normalize_phone(phone: str) -> str:
        """نرمال‌سازی شماره موبایل ایرانی (حذف فاصله و پیش‌شماره +98)."""
        phone = (phone or "").strip().replace(" ", "").replace("-", "")
        if phone.startswith("+98"):
            phone = "0" + phone[3:]
        elif phone.startswith("98") and len(phone) == 12:
            phone = "0" + phone[2:]
        return phone
