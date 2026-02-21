from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language
from markdownx.models import MarkdownxField


class Category(models.Model):
    name = models.CharField(max_length=80)
    name_uz = models.CharField(max_length=80, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

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


class Tag(models.Model):
    name = models.CharField(max_length=60)
    name_uz = models.CharField(max_length=60, blank=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)

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


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    title = models.CharField(max_length=200)
    title_uz = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    excerpt_uz = models.TextField(blank=True)
    content = MarkdownxField()
    content_uz = MarkdownxField(blank=True)
    cover_image = models.ImageField(upload_to="blog/covers/", blank=True, null=True)

    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    meta_title = models.CharField(max_length=160, blank=True)
    meta_title_uz = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    meta_description_uz = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to="blog/og/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_published and not self.published_at:
            from django.utils import timezone

            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def render_markdown(self):
        from .utils import render_markdown

        return render_markdown(self.content_i18n)

    @property
    def title_i18n(self):
        if get_language() == "uz" and self.title_uz:
            return self.title_uz
        return self.title

    @property
    def excerpt_i18n(self):
        if get_language() == "uz" and self.excerpt_uz:
            return self.excerpt_uz
        return self.excerpt

    @property
    def content_i18n(self):
        if get_language() == "uz" and self.content_uz:
            return self.content_uz
        return self.content

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
