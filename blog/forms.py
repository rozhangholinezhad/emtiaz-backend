from django import forms

from .models import Category, Post


class PostForm(forms.ModelForm):
    """فرم ایجاد/ویرایش مقاله."""

    class Meta:
        model = Post
        fields = (
            "title",
            "slug",
            "excerpt",
            "content",
            "cover_image",
            "cover_image_url",
            "category",
            "is_published",
            "is_featured",
        )
        labels = {
            "title": "عنوان",
            "slug": "اسلاگ",
            "excerpt": "خلاصه",
            "content": "متن کامل",
            "cover_image": "تصویر کاور",
            "cover_image_url": "آدرس تصویر کاور",
            "category": "دسته‌بندی",
            "is_published": "منتشر شود",
            "is_featured": "مقاله منتخب",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "w-full rounded-lg border px-3 py-2", "placeholder": "عنوان مقاله"}
            ),
            "slug": forms.TextInput(
                attrs={"class": "w-full rounded-lg border px-3 py-2", "dir": "ltr", "placeholder": "optional-slug"}
            ),
            "excerpt": forms.Textarea(
                attrs={"class": "w-full rounded-lg border px-3 py-2", "rows": 3}
            ),
            "content": forms.Textarea(
                attrs={"class": "w-full rounded-lg border px-3 py-2", "rows": 12}
            ),
            "cover_image_url": forms.URLInput(
                attrs={"class": "w-full rounded-lg border px-3 py-2", "dir": "ltr"}
            ),
            "category": forms.Select(attrs={"class": "w-full rounded-lg border px-3 py-2"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "slug", "description")
        labels = {
            "name": "نام دسته",
            "slug": "اسلاگ",
            "description": "توضیحات",
        }
