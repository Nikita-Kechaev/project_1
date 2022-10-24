from django.contrib import admin

from .models import (
    Callback,
    CallbackDeveloper,
    CallbackInvestor,
    CallbackStartup,
    Case,
    CaseChapter,
    CaseCriterion,
    MOFLMember,
    Project,
    ProjectMember,
    ProjectObjective,
    ProjectStage,
    ProjectVacancy,
    Subscribe,
    VacancyTag,
)


@admin.register(CallbackInvestor)
class CallbackInvestorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "text")
    search_fields = ("name",)


@admin.register(CallbackDeveloper)
class CallbackDeveloperAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "profile",
        "email",
        "competencies",
    )
    search_fields = ("profile",)


@admin.register(CallbackStartup)
class CallbackStartupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "project_title",
        "project_description",
        "file",
    )
    search_fields = ("name",)


@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "interests",
    )
    search_fields = ("name",)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ("email",)
    search_fields = ("email",)


class ProjectMemberAdmin(admin.TabularInline):
    model = ProjectMember
    fields = ("name", "about", "photo")
    extra = 0


class ProjectVacancyAdmin(admin.TabularInline):
    model = ProjectVacancy
    fields = ("title", "description", "image", "tags")
    extra = 0


class ProjectStageAdmin(admin.TabularInline):
    model = ProjectStage
    fields = (
        "year",
        "text",
        "image",
    )
    extra = 0


class ProjectObjectiveAdmin(admin.TabularInline):
    model = ProjectObjective
    fields = (
        "order",
        "title",
        "text",
    )
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    readonly_fields = ("slug", )
    inlines = [
        ProjectMemberAdmin,
        ProjectVacancyAdmin,
        ProjectStageAdmin,
        ProjectObjectiveAdmin,
    ]
    search_fields = (
        "id",
        "title",
    )


class CaseInLineadmin(admin.TabularInline):
    model = Case.similar.through
    extra = 0
    fk_name = "from_case"
    verbose_name = "Похожий кейс"
    verbose_name_plural = "Похожие кейсы"
    max_num = 3


class CaseChapterInLineAdmin(admin.TabularInline):
    model = CaseChapter
    fields = ("title", "description", "image")
    extra = 0


class CaseCriterionInLineAdmin(admin.TabularInline):
    model = CaseCriterion
    fields = ("name",)
    extra = 0


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "date",
    )
    readonly_fields = ("slug", )
    inlines = [
        CaseInLineadmin,
        CaseChapterInLineAdmin,
        CaseCriterionInLineAdmin,
    ]
    search_fields = (
        "id",
        "title",
    )
    exclude = ("similar",)


admin.site.register(VacancyTag)
admin.site.register(MOFLMember)