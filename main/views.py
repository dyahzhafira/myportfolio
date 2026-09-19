from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project

OWNER_NAME = "Dyah Zhafira"


def staff_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url="login",
    )(view_func)


def _admin_form(request, form, page_title):
    return render(
        request,
        "admin/form.html",
        {"name": OWNER_NAME, "form": form, "page_title": page_title},
    )


def _unique_slug(title):
    base = slugify(title) or "project"
    slug, n = base, 2
    while Project.objects.filter(slug=slug).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug



def show_main(request):
    context = {
        "name": "Dyah Zhafira Wibowo",
        "npm": "2506623723",
        "study_program": "S1 Ilmu Komputer",
        "bio": "Hi, I'm Dyah! Let's get to know each other :)",
        "experience_list": Experience.objects.all(),
        "project_list": Project.objects.all(),
    }
    return render(request, "index.html", context)


def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all().order_by("-started_at")

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    return HttpResponse(
        serializers.serialize("json", experiences),
        content_type="application/json",
    )


def show_experience(request):
    json_response = get_experiences_json(request)
    experiences = [
        item.object
        for item in serializers.deserialize("json", json_response.content.decode("utf-8"))
    ]

    context = {
        "name": OWNER_NAME,
        "experience_list": experiences,
        "title_query": request.GET.get("title", "").strip(),
    }
    return render(request, "experience.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    return HttpResponse(
        serializers.serialize("json", projects),
        content_type="application/json",
    )


def show_project(request):
    json_response = get_projects_json(request)
    projects = [
        item.object
        for item in serializers.deserialize("json", json_response.content.decode("utf-8"))
    ]

    context = {
        "name": OWNER_NAME,
        "project_list": projects,
        "title_query": request.GET.get("title", "").strip(),
    }
    return render(request, "project.html", context)


def show_project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(
        request,
        "project_detail.html",
        {"name": OWNER_NAME, "project": project},
    )



@staff_required
def admin_dashboard(request):
    q = request.GET.get("q", "").strip()
    experiences = Experience.objects.all().order_by("-started_at")
    projects = Project.objects.all().order_by("title")

    if q:
        experiences = experiences.filter(title__icontains=q)
        projects = projects.filter(title__icontains=q)

    context = {
        "name": OWNER_NAME,
        "experience_list": experiences,
        "project_list": projects,
        "q": q,
    }
    return render(request, "admin/dashboard.html", context)


@staff_required
def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil ditambahkan!")
        return redirect("main:admin_dashboard")

    return _admin_form(request, form, "Add Experience")


@staff_required
def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:admin_dashboard")

    return _admin_form(request, form, "Edit Experience")


@staff_required
@require_POST
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id)
    experience.delete()
    messages.success(request, "Experience berhasil dihapus!")
    return redirect("main:admin_dashboard")


@staff_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.slug = _unique_slug(project.title)
        project.tech_stack = []
        project.save()
        messages.success(request, "Project berhasil ditambahkan!")
        return redirect("main:admin_dashboard")

    return _admin_form(request, form, "Add Project")


@staff_required
def update_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project berhasil diperbarui!")
        return redirect("main:admin_dashboard")

    return _admin_form(request, form, "Edit Project")


@staff_required
@require_POST
def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.delete()
    messages.success(request, "Project berhasil dihapus!")
    return redirect("main:admin_dashboard")
