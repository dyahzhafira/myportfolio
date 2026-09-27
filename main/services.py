from django.core import serializers
from django.http import HttpResponse
from django.utils.text import slugify

from main.models import Project


def filter_by_title(queryset, query):
    """filter queryset based on judul"""
    query = (query or "").strip()
    return queryset.filter(title__icontains=query) if query else queryset


def json_response(queryset, exclude=None):
    """serialize queryset model to HttpResponse format JSON, exclude field tertentu kalau ada"""
    fields = None
    if exclude:
        fields = [
            field.name
            for field in queryset.model._meta.get_fields()
            if field.concrete and field.name not in exclude
        ]
    return HttpResponse(
        serializers.serialize(
            "json", queryset, use_natural_foreign_keys=True, fields=fields
        ),
        content_type="application/json",
    )


def objects_from_json(response):
    """deserialize isi HttpResponse JSON jadi list objek model."""
    payload = response.content.decode("utf-8")
    return [item.object for item in serializers.deserialize("json", payload)]


def unique_slug(title):
    """buat slug dari judul, tambah angka kalau udah dipake"""
    base = slugify(title) or "project"
    slug, n = base, 2
    while Project.objects.filter(slug=slug).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug
