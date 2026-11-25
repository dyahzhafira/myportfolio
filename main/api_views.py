from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Experience, Project
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import ExperienceSerializer, ProjectSerializer
from main.services import filter_by_title


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        projects = filter_by_title(
            Project.objects.prefetch_related("starred_by").order_by("title", "id"),
            request.query_params.get("title", ""),
        )
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request},
        )
        data = serializer.data
        if request.query_params.get("sort") == "star":
            data = sorted(data, key=lambda item: item["star_count"], reverse=True)
        return Response(data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    serializer = ProjectSerializer(project, context={"request": request})
    return Response(serializer.data)


@api_view(["GET", "HEAD", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    """GET: daftar + ?title= ?category= ?sort=star; POST: buat (owner)."""
    if request.method in ("GET", "HEAD"):
        experiences = Experience.objects.prefetch_related("starred_by")
        category = request.query_params.get("category", "").strip()
        if category:
            experiences = experiences.filter(category=category)
        experiences = filter_by_title(experiences, request.query_params.get("title", ""))
        if request.query_params.get("sort") == "star":
            experiences = experiences.annotate(n_stars=Count("starred_by")).order_by(
                "-n_stars", "-started_at"
            )
        else:
            experiences = experiences.order_by("-started_at")
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    """GET/PUT/PATCH/DELETE satu Experience; Editor hanya boleh PUT/PATCH."""
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id,
    )
    if request.method in ("GET", "HEAD"):
        return Response(ExperienceSerializer(experience, context={"request": request}).data)

    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    """Toggle star Experience; akun selalu dari request.user."""
    experience = get_object_or_404(Experience, pk=experience_id)
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)
    return Response(ExperienceSerializer(experience, context={"request": request}).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_logout(request):
    if request.auth is not None:
        request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
