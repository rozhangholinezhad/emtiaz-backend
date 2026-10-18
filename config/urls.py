"""
URL configuration for config project.
"""
from django.conf.urls import static
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include("accounts.urls")),
    path('blog/', include("blog.urls")),
    path('real_estate/', include("real_estate.urls")),
    path('dashbord/', include("dashbord.urls")),

=======
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("blog/", include("blog.urls")),
    path("real_estate/", include("real_estate.urls")),
    path("dashbord/", include("dashbord.urls")),
>>>>>>> 44d8d2ff8010c5c2e8331de832cb29c1e109c247
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)