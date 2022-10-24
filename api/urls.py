from django.urls import include, path
from rest_framework import routers

from .views import CallbackViewSet, CaseViewSet, ProjectViewSet, SubscribeViewSet, TeamViewSet

app_name = "api"

router_v1 = routers.DefaultRouter()
router_v1.register("callback", CallbackViewSet, basename="callback")
router_v1.register("subscribe", SubscribeViewSet, basename="subscribe")
router_v1.register("projects", ProjectViewSet, basename="projects")
router_v1.register("cases", CaseViewSet, basename="cases")
router_v1.register("team", TeamViewSet, basename="team")


urlpatterns = [
    path("", include(router_v1.urls)),
]
