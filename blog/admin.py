from django.contrib import admin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "is_published",
        "is_featured",
        "published_at",
        "views_count",
    )
    list_filter = ("is_published", "is_featured", "category", "published_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("views_count", "created_at", "updated_at")
    date_hierarchy = "published_at"
    autocomplete_fields = ("category", "author")
    fieldsets = (
        ("محتوا", {"fields": ("title", "slug", "excerpt", "content")}),
        ("رسانه", {"fields": ("cover_image", "cover_image_url")}),
        ("طبقه‌بندی و نویسنده", {"fields": ("category", "author")}),
        ("انتشار", {"fields": ("is_published", "is_featured", "published_at")}),
        ("آمار", {"fields": ("views_count", "created_at", "updated_at")}),
    )
