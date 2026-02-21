from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language


class ProjectCategory(models.Model):
    name = models.CharField(max_length=80)
    name_uz = models.CharField(max_length=80, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def __str__(self) -> str:
        return self.name

    @property
    def name_i18n(self):
        if get_language() == "uz" and self.name_uz:
            return self.name_uz
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects"
    )
    title = models.CharField(max_length=200)
    title_uz = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    description_uz = models.TextField(blank=True)
    tech_stack = models.TextField(help_text="Comma-separated tech stack")
    tech_stack_uz = models.TextField(blank=True, help_text="Comma-separated tech stack")
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    year = models.PositiveIntegerField(default=2025)
    featured = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to="projects/covers/", blank=True, null=True)

    meta_title = models.CharField(max_length=160, blank=True)
    meta_title_uz = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    meta_description_uz = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to="projects/og/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "title"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def title_i18n(self):
        if get_language() == "uz" and self.title_uz:
            return self.title_uz
        return self.title

    @property
    def description_i18n(self):
        if get_language() == "uz" and self.description_uz:
            return self.description_uz
        return self.description

    @property
    def meta_title_i18n(self):
        if get_language() == "uz" and self.meta_title_uz:
            return self.meta_title_uz
        return self.meta_title

    @property
    def meta_description_i18n(self):
        if get_language() == "uz" and self.meta_description_uz:
            return self.meta_description_uz
        return self.meta_description

    @property
    def tech_list(self):
        stack = self.tech_stack_uz if get_language() == "uz" and self.tech_stack_uz else self.tech_stack
        return [item.strip() for item in stack.split(",") if item.strip()]


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/gallery/")
    alt_text = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return f"{self.project.title} image"
