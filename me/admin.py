from django.contrib import admin
from .models import ContactMessage, Profile, Skill, Stat, TimelineItem


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "full_name", "role", "email", "updated_at")
    search_fields = ("name", "full_name", "role", "email")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "full_name",
                    "name",
                    "role",
                    "role_uz",
                    "tagline",
                    "tagline_uz",
                    "bio",
                    "bio_uz",
                    "skills_text",
                )
            },
        ),
        (
            "Contact",
            {
                "fields": (
                    "email",
                    "phone",
                    "telegram",
                    "github",
                )
            },
        ),
        (
            "Media",
            {
                "fields": (
                    "avatar",
                    "cv",
                )
            },
        ),
        (
            "Other",
            {
                "fields": (
                    "date_of_birth",
                    "location",
                )
            },
        ),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "category", "profile")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(TimelineItem)
class TimelineItemAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "type", "start_date", "end_date", "is_current")
    list_filter = ("type", "is_current")
    search_fields = ("title", "organization")


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "suffix", "profile")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)
