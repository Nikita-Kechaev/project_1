from rest_framework import serializers

from .models import (
    Callback,
    CallbackDeveloper,
    CallbackInvestor,
    CallbackStartup,
    Case,
    CaseChapter,
    Project,
    ProjectMember,
    ProjectObjective,
    ProjectStage,
    ProjectVacancy,
    Subscribe,
    MOFLMember,
)


class CallbackInvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallbackInvestor
        fields = "__all__"


class CallbackDeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallbackDeveloper
        fields = "__all__"


class CallbackStartupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallbackStartup
        fields = "__all__"


class CallbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Callback
        fields = "__all__"


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = "__all__"


class MOFLMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MOFLMember
        fields = "__all__"


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = "__all__"


class ProjectVacancySerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field="title",
        read_only=True
    )

    class Meta:
        model = ProjectVacancy
        fields = "__all__"


class ProjectObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectObjective
        fields = "__all__"


class ProjectStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStage
        fields = "__all__"


class ProjectListSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "thumbnail",
            "title",
            "slug",
            "short_description"
        )


class ProjectRetrieveSerializer(serializers.ModelSerializer):
    members = ProjectMemberSerializer(many=True, read_only=True)
    vacancies = ProjectVacancySerializer(many=True, read_only=True)
    stages = ProjectStageSerializer(many=True, read_only=True)
    objectives = ProjectObjectiveSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "banner",
            "description",
            "seo_description",
            "presentation",
            "required_investments",
            "current_investments",
            "members",
            "vacancies",
            "stages",
            "objectives",
        )


class CaseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseChapter
        fields = "__all__"


class CaseSimilarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = (
            "id",
            "thumbnail",
            "title",
            "short_description",
        )


class CaseListSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Case
        fields = (
            "id",
            "title",
            "slug",
            "short_description",
            "thumbnail",
        )


class CaseRetrieveSerializer(serializers.ModelSerializer):
    similar = CaseSimilarSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = (
            "id",
            "title",
            "thumbnail",
            "description",
            "seo_description",
            "client",
            "objective",
            "solution",
            "date",
            "similar",
        )


class CaseRetrieveDetailSerializer(serializers.ModelSerializer):
    similar = CaseSimilarSerializer(many=True, read_only=True)
    chapters = CaseChapterSerializer(many=True, read_only=True)
    criteria = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
    )

    class Meta:
        model = Case
        fields = (
            "id",
            "title",
            "thumbnail",
            "description",
            "seo_description",
            "client",
            "objective",
            "solution",
            "date",
            "similar",
            "chapters",
            "criteria",
        )
