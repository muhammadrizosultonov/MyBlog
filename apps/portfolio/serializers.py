from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "tech_stack",
            "tech_list",
            "github_url",
            "live_url",
            "year",
            "featured",
        ]
