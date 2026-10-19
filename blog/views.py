from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Q
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Category, Post


class PostListView(ListView):
    """لیست مقالات منتشرشده."""

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        qs = (
            Post.objects.filter(is_published=True)
            .select_related("category", "author")
            .order_by("-published_at", "-created_at")
        )
        category_slug = self.request.GET.get("category")
        q = self.request.GET.get("q")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(excerpt__icontains=q)
                | Q(content__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["featured_post"] = (
            Post.objects.filter(is_published=True, is_featured=True)
            .select_related("category", "author")
            .order_by("-published_at")
            .first()
        )
        ctx["active_category"] = self.request.GET.get("category", "")
        ctx["search_query"] = self.request.GET.get("q", "")
        return ctx


class PostDetailView(DetailView):
    """جزئیات مقاله."""

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        qs = Post.objects.select_related("category", "author")
        user = self.request.user
        if user.is_authenticated and (
            user.is_staff or getattr(user, "can_publish_article", False)
        ):
            return qs
        return qs.filter(is_published=True)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Post.objects.filter(pk=obj.pk).update(views_count=F("views_count") + 1)
        obj.refresh_from_db(fields=["views_count"])
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["related_posts"] = (
            Post.objects.filter(is_published=True)
            .exclude(pk=self.object.pk)
            .filter(category=self.object.category)
            .select_related("category")[:3]
        )
        return ctx


class StaffPublishMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_staff or getattr(u, "can_publish_article", False)


class PostCreateView(StaffPublishMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostUpdateView(StaffPublishMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return self.object.get_absolute_url()
