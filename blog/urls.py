from django.urls import path, register_converter

from .views import PostCreateView, PostDetailView, PostListView, PostUpdateView


class UnicodeSlugConverter:
    """Accept Latin and Persian characters in slugs."""

    # letters, numbers, underscore, hyphen, Arabic/Persian script
    regex = r"[-a-zA-Z0-9_\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(UnicodeSlugConverter, "uslug")

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("new/", PostCreateView.as_view(), name="post_create"),
    path("<uslug:slug>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("<uslug:slug>/", PostDetailView.as_view(), name="post_detail"),
]
