from slugify import slugify

from django.db import models


class CallbackInvestor(models.Model):
    name = models.CharField(verbose_name="ФИО", max_length=255)
    email = models.TextField(verbose_name="Электронная почта")
    phone = models.CharField(verbose_name="Номер телефона", max_length=255)
    text = models.TextField(verbose_name="Сообщение")

    class Meta:
        verbose_name = "Заявка от инвестора"
        verbose_name_plural = "Заявки от инвесторов"

    def __str__(self):
        return f"Заявка инвестора: {self.name}"


class CallbackDeveloper(models.Model):
    name = models.CharField(verbose_name="ФИО", max_length=255)
    profile = models.CharField(verbose_name="Профиль разработчика", max_length=255)
    email = models.TextField(verbose_name="Электронная почта")
    competencies = models.TextField(verbose_name="Компетенции")

    class Meta:
        verbose_name = "Заявка от разработчика"
        verbose_name_plural = "Заявки от разработчиков"

    def __str__(self):
        return f"Заявка разработчика: {self.profile}"


class CallbackStartup(models.Model):
    name = models.CharField(max_length=255, verbose_name="ФИО")
    email = models.TextField(verbose_name="Электронная почта")
    project_title = models.TextField(verbose_name="Название проекта")
    project_description = models.TextField(verbose_name="Описание проекта")
    file = models.FileField(verbose_name="Прикрепленный файл")

    class Meta:
        verbose_name = "Заявка от стартапа"
        verbose_name_plural = "Заявки от стартапов"

    def __str__(self):
        return f"Заявка cтартапа: {self.project_title}"


class Callback(models.Model):
    name = models.CharField(verbose_name="ФИО / Название", max_length=255)
    phone = models.TextField(verbose_name="Номер телефона")
    interests = models.TextField(verbose_name="Что интересует посетителя")

    class Meta:
        verbose_name = "Обратая связь от посетителя сайта"
        verbose_name_plural = "Обратая связь от посетителей сайта"

    def __str__(self):
        return f"Отклик: {self.name}"


class Subscribe(models.Model):
    email = models.TextField(verbose_name="Email")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return "Подписка на: " + self.email


class Project(models.Model):
    title = models.CharField(
        verbose_name="Название проекта", max_length=255, unique=True
    )
    slug = models.SlugField(unique=True)
    banner = models.ImageField(verbose_name="Заглавный баннер проекта")
    thumbnail = models.ImageField(verbose_name="Мини - изображение проекта")
    description = models.TextField(verbose_name="Описание проекта")
    seo_description = models.TextField(verbose_name="SEO описание проекта")
    short_description = models.TextField(verbose_name="Краткое описание проекта")
    presentation = models.FileField(verbose_name="Файл с презентацией проекта")
    required_investments = models.IntegerField(verbose_name="Требуемая сумма")
    current_investments = models.IntegerField(verbose_name="Собранная сумма")
    is_popular = models.BooleanField(
        verbose_name="Популярный кейс?",
        default=False,
        help_text="Определяет будет ли отображаться данный проект в блоке \"Популярные проекты\""
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Проект: {self.title}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("api:projects-detail", kwargs={"slug" : self.slug})


class ProjectMember(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Участвует в проекте",
    )
    photo = models.ImageField(verbose_name="Фотография участника")
    name = models.CharField(verbose_name="Имя участника", max_length=255)
    about = models.TextField(verbose_name="Об участнике")

    class Meta:
        verbose_name = "Участник проекта"
        verbose_name_plural = "Участники проекта"

    def __str__(self):
        return f"Участник проекта: {self.name}"


class VacancyTag(models.Model):
    title = models.CharField(max_length=255, verbose_name="Компетенция", unique=True)

    class Meta:
        verbose_name = "Тэг для вакансии"
        verbose_name_plural = "Тэги вакансий"

    def __str__(self) -> str:
        return self.title


class ProjectVacancy(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="vacancies",
        verbose_name="Вакансии в проекте",
    )
    tags = models.ManyToManyField(VacancyTag, verbose_name="Тэги вакансии")
    image = models.ImageField(verbose_name="Изображение вакансии")
    title = models.CharField(max_length=255, verbose_name="Название вакансии")
    description = models.TextField(verbose_name="Описание вакансии")

    class Meta:
        verbose_name = "Вакансия в проекте"
        verbose_name_plural = "Вакансии в проекте"

    def __str__(self) -> str:
        return f"Вакансия: {self.title}"


class ProjectStage(models.Model):
    # в данной модели добавить поле с указанием текущей стадии?
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="stages",
        verbose_name="Вакансии в проекте",
    )
    # можно реализовать выбор конкретного года(из промежутка)
    year = models.IntegerField(verbose_name="Год реализации")
    image = models.ImageField(verbose_name="Картинка стадии проекта")
    text = models.TextField(verbose_name="Текст под картинкой стадии")

    class Meta:
        verbose_name = "Стадия проекта"
        verbose_name_plural = "Cтадии проекта"

    def __str__(self) -> str:
        return f"Стадия проекта {self.project} на {self.year} год."


class ProjectObjective(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="objectives",
        verbose_name="Вакансии в проекте",
    )
    order = models.IntegerField(verbose_name="Номер цели")
    title = models.CharField(max_length=255, verbose_name="Цель - заголовок")
    text = models.TextField(verbose_name="Описание цели инвестиций")

    class Meta:
        verbose_name = "Цель проекта"
        verbose_name_plural = "Цели проекта"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "order"], name="unique order for project"
            )
        ]

    def __str__(self) -> str:
        return f"Цель: {self.title} проекта {self.project}"


class MOFLMember(models.Model):
    photo = models.ImageField(verbose_name="Фотография участника")
    name = models.CharField(verbose_name="Имя участника", max_length=255)
    about = models.TextField(verbose_name="Об участнике")

    class Meta:
        verbose_name = "Участник MOFL"
        verbose_name_plural = "Участники MOFL"

    def __str__(self):
        return f"Участник проекта: {self.name}"


class Case(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название кейса")
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(verbose_name="Уменьшенное изображение кейса")
    short_description = models.TextField(verbose_name="Короткое описание кейса")
    description = models.TextField(verbose_name="Описание кейса")
    seo_description = models.TextField(verbose_name="SEO описание проекта")
    client = models.CharField(max_length=255, verbose_name="Клиент")
    objective = models.TextField(verbose_name="Цели кейса")
    solution = models.TextField(verbose_name="Решение")
    date = models.DateField(verbose_name="Дата создания кейса")
    similar = models.ManyToManyField(
        "Case", verbose_name="Похожие кейсы", blank=True, symmetrical=True
    )

    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = "Кейсы"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Кейс: {self.title}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("api:case-detail", kwargs={"slug" : self.slug})


class CaseChapter(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="chapters",
        verbose_name="Пункты кейса",
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок пункта")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Картинка пункта")

    class Meta:
        verbose_name = "Пункт кейса"
        verbose_name_plural = "Пункты кейса"

    def __str__(self) -> str:
        return f"Пункт кейса: {self.title}"


class CaseCriterion(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="criteria",
        verbose_name="Кейс"
    )
    name = models.CharField(verbose_name="Название критерия", max_length=120)

    class Meta:
        verbose_name = "Критерий кейса"
        verbose_name_plural = "Критерии кейса"

    def __str__(self) -> str:
        return f"Критерий кейса: {self.name}"
