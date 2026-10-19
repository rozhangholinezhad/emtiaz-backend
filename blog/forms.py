from django import forms

from .models import Category, Post

FIELD_CLASS = (
    "w-full rounded-lg border border-outline-variant px-3 py-2 text-sm "
    "focus:outline-none focus:ring-2 focus:ring-secondary/30 focus:border-primary"
)


class PostForm(forms.ModelForm):
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
            "slug": "اسلاگ (اختیاری)",
            "excerpt": "خلاصه",
            "content": "متن کامل",
            "cover_image": "تصویر کاور",
            "cover_image_url": "آدرس تصویر کاور (URL)",
            "category": "دسته‌بندی",
            "is_published": "منتشر شود",
            "is_featured": "مقاله منتخب",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": FIELD_CLASS, "placeholder": "عنوان مقاله"}),
            "slug": forms.TextInput(
                attrs={
                    "class": FIELD_CLASS,
                    "dir": "ltr",
                    "placeholder": "خالی بگذارید تا خودکار ساخته شود",
                }
            ),
            "excerpt": forms.Textarea(attrs={"class": FIELD_CLASS, "rows": 3}),
            "content": forms.Textarea(attrs={"class": FIELD_CLASS, "rows": 12}),
            "cover_image_url": forms.URLInput(attrs={"class": FIELD_CLASS, "dir": "ltr"}),
            "category": forms.Select(attrs={"class": FIELD_CLASS}),
            "cover_image": forms.ClearableFileInput(attrs={"class": "text-sm"}),
            "is_published": forms.CheckboxInput(attrs={"class": "rounded border-outline-variant"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "rounded border-outline-variant"}),
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
        widgets = {
            "name": forms.TextInput(attrs={"class": FIELD_CLASS, "placeholder": "نام دسته‌بندی"}),
            "slug": forms.TextInput(
                attrs={"class": FIELD_CLASS, "dir": "ltr", "placeholder": "اختیاری"}
            ),
            "description": forms.Textarea(attrs={"class": FIELD_CLASS, "rows": 2}),
        }
