from django.shortcuts import render, get_object_or_404

from main.models import Experience, Project
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from main.forms import ProjectForm



def show_main(request):
    context = {
        "name": "Dyah Zhafira Wibowo",
        "npm": "2506623723",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Hi, I'm Dyah! Let's get to know each other :)"
        ),
        "experience_list": Experience.objects.all(),
        "project_list": Project.objects.all(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Dyah Zhafira",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {
        "name": "Dyah Zhafira",
        "project": project,
    }
    return render(request, "project_detail.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.slug = slugify(project.title)
        project.tech_stack = []
        project.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")

    context = {
        "name": "Dyah Zhafira",
        "form": form,
    }
    return render(request, "projects_form.html", context)


def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def show_project(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Dyah Zhafira",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)
