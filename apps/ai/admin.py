from django.contrib import admin
from .models import AIChatLog, AssistantLog


@admin.register(AIChatLog)
class AIChatLogAdmin(admin.ModelAdmin):
    list_display = ("session_id", "ip_address", "created_at", "is_blocked")
    list_filter = ("is_blocked", "created_at")
    search_fields = ("session_id", "question", "answer")
    readonly_fields = (
        "session_id",
        "ip_address",
        "question",
        "answer",
        "model",
        "prompt_tokens",
        "completion_tokens",
        "is_blocked",
        "blocked_reason",
        "created_at",
    )


@admin.register(AssistantLog)
class AssistantLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "status", "provider", "model_used", "tokens_used", "latency_ms", "created_at")
    search_fields = ("ip_address", "message", "answer", "model_used", "provider")
    readonly_fields = (
        "ip_address",
        "message",
        "answer",
        "status",
        "provider",
        "model_used",
        "tokens_used",
        "latency_ms",
        "created_at",
    )
