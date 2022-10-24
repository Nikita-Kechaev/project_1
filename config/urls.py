from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        "docs/",
        login_required(
            TemplateView.as_view(
                template_name="docs.html",
            )
        )
    )
]
