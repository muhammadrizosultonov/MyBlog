from django.db import models
from django.utils.translation import get_language
from django.utils.text import slugify


class Profile(models.Model):
    full_name = models.CharField(max_length=160, blank=True)
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=160)
    role_uz = models.CharField(max_length=160, blank=True)
    tagline = models.CharField(max_length=240)
    tagline_uz = models.CharField(max_length=240, blank=True)
    bio = models.TextField(blank=True)
    bio_uz = models.TextField(blank=True)
    skills_text = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    telegram = models.CharField(max_length=120, blank=True)
    github = models.URLField(blank=True)
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True)
    cv = models.FileField(upload_to="cv/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self) -> str:
        return self.name

    @property
    def role_i18n(self):
        if get_language() == "uz" and self.role_uz:
            return self.role_uz
        return self.role

    @property
    def tagline_i18n(self):
        if get_language() == "uz" and self.tagline_uz:
            return self.tagline_uz
        return self.tagline

    @property
    def bio_i18n(self):
        if get_language() == "uz" and self.bio_uz:
            return self.bio_uz
        return self.bio


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(default=70)
    category = models.CharField(max_length=80, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.level}%)"


class TimelineItem(models.Model):
    TYPE_CHOICES = (
        ("experience", "Experience"),
        ("education", "Education"),
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="timeline")
    title = models.CharField(max_length=160)
    organization = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="experience")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-is_current", "-start_date", "order"]

    def __str__(self) -> str:
        return f"{self.title}"


class Stat(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="stats")
    label = models.CharField(max_length=80)
    value = models.PositiveIntegerField(default=0)
    suffix = models.CharField(max_length=10, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.label}: {self.value}{self.suffix}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.subject}"
