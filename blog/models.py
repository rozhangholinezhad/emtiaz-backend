from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """دسته‌بندی مقالات وبلاگ."""

    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته")
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Post(models.Model):
    """مقاله وبلاگ املاک امتیاز."""

    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(
        max_length=280,
        unique=True,
        allow_unicode=True,
        verbose_name="اسلاگ",
        help_text="برای URL؛ در صورت خالی بودن از عنوان ساخته می‌شود.",
    )
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="خلاصه",
        help_text="متن کوتاه برای کارت لیست مقالات.",
    )
    content = models.TextField(verbose_name="متن کامل")
    cover_image = models.ImageField(
        upload_to="blog/covers/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="تصویر کاور",
    )
    cover_image_url = models.URLField(
        blank=True,
        verbose_name="آدرس تصویر کاور (خارجی)",
        help_text="اگر تصویر آپلود نشده، می‌توان از URL استفاده کرد.",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="دسته‌بندی",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
        verbose_name="نویسنده",
    )
    is_published = models.BooleanField(default=False, verbose_name="منتشر شده")
    is_featured = models.BooleanField(default=False, verbose_name="مقاله منتخب")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="زمان انتشار")
    views_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["-published_at", "is_published"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title, allow_unicode=True) or "post"
            candidate = base
            n = 1
            while Post.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                n += 1
                candidate = f"{base}-{n}"
            self.slug = candidate
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    @property
    def cover(self):
        if self.cover_image:
            return self.cover_image.url
        return self.cover_image_url or ""
