from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django import forms

from blog.models import Category, Post

User = get_user_model()


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """صفحه اصلی داشبورد مدیریت."""

    template_name = "dashbord/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        posts_total = Post.objects.count()
        posts_published = Post.objects.filter(is_published=True).count()
        categories_count = Category.objects.count()
        users_count = User.objects.count()

        ctx.update(
            {
                "page_title": "نمای کلی",
                "breadcrumb": "داشبورد",
                "stats": {
                    "properties_total": 0,
                    "properties_published": 0,
                    "offices_active": 0,
                    "posts_total": posts_total,
                    "posts_published": posts_published,
                    "categories_count": categories_count,
                    "users_count": users_count,
                    "contact_requests": 0,
                    "media_count": 0,
                },
                "recent_posts": (
                    Post.objects.select_related("category", "author")
                    .order_by("-created_at")[:5]
                ),
                "today_display": timezone.localdate(),
                "active_nav": "dashboard",
            }
        )
        return ctx


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone")
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "phone": "شماره موبایل",
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "w-full rounded-lg border border-outline-variant px-3 py-2 text-sm"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "w-full rounded-lg border border-outline-variant px-3 py-2 text-sm"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-outline-variant px-3 py-2 text-sm",
                    "dir": "ltr",
                }
            ),
        }


class DashboardProfileView(LoginRequiredMixin, UpdateView):
    """پروفایل کاربر داخل داشبورد."""

    model = User
    form_class = ProfileForm
    template_name = "dashbord/profile.html"
    success_url = reverse_lazy("dashbord:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "پروفایل"
        ctx["breadcrumb"] = "حساب کاربری"
        ctx["active_nav"] = "profile"
        return ctx

    def form_valid(self, form):
        from django.contrib import messages

        messages.success(self.request, "پروفایل با موفقیت به‌روزرسانی شد.")
        return super().form_valid(form)
