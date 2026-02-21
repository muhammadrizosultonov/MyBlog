from django.db import models


class AIChatLog(models.Model):
    session_id = models.CharField(max_length=120, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    model = models.CharField(max_length=120, blank=True)
    prompt_tokens = models.PositiveIntegerField(default=0)
    completion_tokens = models.PositiveIntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    blocked_reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.session_id} - {self.created_at:%Y-%m-%d %H:%M}"


class AssistantLog(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    message = models.TextField()
    answer = models.TextField()
    status = models.CharField(max_length=20, default="ok")
    model_used = models.CharField(max_length=120, blank=True)
    tokens_used = models.PositiveIntegerField(null=True, blank=True)
    provider = models.CharField(max_length=20, blank=True)
    latency_ms = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.ip_address} - {self.created_at:%Y-%m-%d %H:%M}"
