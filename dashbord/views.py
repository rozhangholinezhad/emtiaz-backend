from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from blog.forms import CategoryForm, PostForm
from blog.models import Category, Post

User = get_user_model()


class DashboardAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    """دسترسی به بخش مدیریت محتوا."""

    def test_func(self):
        u = self.request.user
        return bool(u.is_staff or getattr(u, "can_publish_article", False) or u.is_employee)


class DashboardHomeView(LoginRequiredMixin, TemplateView):
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
                "recent_posts": Post.objects.select_related("category", "author").order_by(
                    "-created_at"
                )[:5],
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
        messages.success(self.request, "پروفایل با موفقیت به‌روزرسانی شد.")
        return super().form_valid(form)


class DashboardPostListView(DashboardAccessMixin, ListView):
    model = Post
    template_name = "dashbord/blog_list.html"
    context_object_name = "posts"
    paginate_by = 15

    def get_queryset(self):
        qs = Post.objects.select_related("category", "author").order_by("-created_at")
        q = self.request.GET.get("q")
        status = self.request.GET.get("status")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q))
        if status == "published":
            qs = qs.filter(is_published=True)
        elif status == "draft":
            qs = qs.filter(is_published=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "مدیریت مقالات"
        ctx["breadcrumb"] = "وبلاگ"
        ctx["active_nav"] = "blog"
        ctx["search_query"] = self.request.GET.get("q", "")
        ctx["status_filter"] = self.request.GET.get("status", "")
        return ctx


class DashboardPostCreateView(DashboardAccessMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashbord/blog_form.html"
    success_url = reverse_lazy("dashbord:blog_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "مقاله با موفقیت ایجاد شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "افزودن مقاله"
        ctx["breadcrumb"] = "وبلاگ"
        ctx["active_nav"] = "blog"
        ctx["is_edit"] = False
        return ctx


class DashboardPostUpdateView(DashboardAccessMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashbord/blog_form.html"
    success_url = reverse_lazy("dashbord:blog_list")
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        messages.success(self.request, "مقاله با موفقیت ویرایش شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "ویرایش مقاله"
        ctx["breadcrumb"] = "وبلاگ"
        ctx["active_nav"] = "blog"
        ctx["is_edit"] = True
        return ctx


class DashboardPostDeleteView(DashboardAccessMixin, DeleteView):
    model = Post
    template_name = "dashbord/blog_confirm_delete.html"
    success_url = reverse_lazy("dashbord:blog_list")
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        messages.success(self.request, "مقاله حذف شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "حذف مقاله"
        ctx["breadcrumb"] = "وبلاگ"
        ctx["active_nav"] = "blog"
        return ctx


class DashboardCategoryListView(DashboardAccessMixin, ListView):
    model = Category
    template_name = "dashbord/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "دسته‌بندی مقالات"
        ctx["breadcrumb"] = "وبلاگ"
        ctx["active_nav"] = "categories"
        ctx["form"] = CategoryForm()
        return ctx


class DashboardCategoryCreateView(DashboardAccessMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashbord/category_list.html"
    success_url = reverse_lazy("dashbord:category_list")

    def form_valid(self, form):
        messages.success(self.request, "دسته‌بندی ایجاد شد.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "خطا در ایجاد دسته‌بندی. نام تکراری نباشد.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["page_title"] = "دسته‌بندی مقالات"
        ctx["breadcrumb"] = "وبلاگ"
        ctx["active_nav"] = "categories"
        return ctx


class DashboardCategoryDeleteView(DashboardAccessMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("dashbord:category_list")
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        messages.success(self.request, "دسته‌بندی حذف شد.")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
