from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Project
from main.services import unique_slug


class StarFieldsMixin(serializers.Serializer):
    """Field star read-only yang dipakai bersama Project dan Experience."""

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class ProjectSerializer(StarFieldsMixin, serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    project_type_display = serializers.CharField(
        source="get_project_type_display", read_only=True
    )

    class Meta:
        model = Project
        fields = [
            "id", "slug", "title", "description",
            "status", "status_display", "project_type", "project_type_display",
            "tech_stack", "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "slug", "tech_stack"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def create(self, validated_data):
        validated_data["slug"] = unique_slug(validated_data["title"])
        return super().create(validated_data)


class ExperienceSerializer(StarFieldsMixin, serializers.ModelSerializer):
    """Representasi dan validasi Experience; ended_at null berarti masih berlangsung."""

    category_display = serializers.CharField(source="get_category_display", read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description",
            "category", "category_display", "thumbnail",
            "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()
