from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Case, Project, MOFLMember
from .serializers import (
    CallbackDeveloperSerializer,
    CallbackInvestorSerializer,
    CallbackSerializer,
    CallbackStartupSerializer,
    CaseListSerializer,
    CaseRetrieveDetailSerializer,
    CaseRetrieveSerializer,
    ProjectListSerializer,
    ProjectRetrieveSerializer,
    SubscribeSerializer,
    MOFLMemberSerializer,
)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 18
    page_size_query_param = 'page_size'
    max_page_size = 100


class TeamViewSet(viewsets.GenericViewSet):
    queryset = MOFLMember.objects.all()
    serializer_class = MOFLMemberSerializer

    def list(self, request):
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CallbackViewSet(viewsets.GenericViewSet):
    serializer_class = CallbackSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        url_name="investors",
        url_path="investors",
        serializer_class=CallbackInvestorSerializer,
    )
    def investors(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        url_name="developers",
        url_path="developers",
        serializer_class=CallbackDeveloperSerializer,
    )
    def developers(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        url_name="startups",
        url_path="startups",
        serializer_class=CallbackStartupSerializer,
    )
    def startups(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscribeViewSet(viewsets.GenericViewSet):
    serializer_class = SubscribeSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.GenericViewSet):
    queryset = Project.objects.all()
    pagination_class = CustomPageNumberPagination
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action in ["list", "populars"]:
            return ProjectListSerializer
        return ProjectRetrieveSerializer

    def list(self, request):
        serializer = self.get_serializer_class()
        page = self.paginate_queryset(self.get_queryset())
        serializer = serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, slug=None):
        serializer = self.get_serializer_class()
        project = self.get_object()
        serializer = serializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_name="populars",
        url_path="populars",
        queryset=Project.objects.filter(is_popular=True)
    )
    def populars(self, request):
        serializer = self.get_serializer_class()
        projects = self.get_queryset()
        serializer = serializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_name="latest",
        url_path="latest",
        queryset=Project.objects.all().order_by("-id")
    )
    def latest(self, request):
        serializer = self.get_serializer_class()
        page = self.paginate_queryset(self.get_queryset())
        serializer = serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CaseViewSet(viewsets.GenericViewSet):
    queryset = Case.objects.all()
    pagination_class = CustomPageNumberPagination
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return CaseListSerializer
        elif self.action == "retrieve":
            return CaseRetrieveSerializer
        return CaseRetrieveDetailSerializer

    def list(self, request):
        serializer = self.get_serializer_class()
        page = self.paginate_queryset(self.get_queryset())
        serializer = serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, slug=None):
        serializer = self.get_serializer_class()
        case = self.get_object()
        serializer = serializer(case)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_name="details",
        url_path="details",
    )
    def details(self, request, slug=None):
        serializer = self.get_serializer_class()
        case = self.get_object()
        serializer = serializer(case)
        return Response(serializer.data, status=status.HTTP_200_OK)
