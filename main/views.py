from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project
from main.services import filter_by_title, json_response, objects_from_json, unique_slug

OWNER_NAME = "Dyah Zhafira"


def staff_required(view_func):
    """batasi view untuk user staff, sisanya ke login"""
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url="login",
    )(view_func)


def _title_query(request):
    """ambil keyword title dari query string."""
    return request.GET.get("title", "").strip()


def _admin_form(request, form, page_title):
    """render form admin tambah atau ubah data."""
    return render(
        request,
        "admin/form.html",
        {"name": OWNER_NAME, "form": form, "page_title": page_title},
    )


def _handle_form(request, form, page_title, success_message):
    """save form if valid"""
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, success_message)
        return redirect("main:admin_dashboard")
    return _admin_form(request, form, page_title)


def _delete_and_redirect(instance, success_message, request):
    """hapus objek return to dashboard + success message"""
    instance.delete()
    messages.success(request, success_message)
    return redirect("main:admin_dashboard")


# Public pages

def show_main(request):
    """main page"""
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
    """return data Experience dalam JSON"""
    queryset = Experience.objects.order_by("-started_at")
    return json_response(filter_by_title(queryset, _title_query(request)))


def show_experience(request):
    """show Experience dari JSON yang di deserialize + search"""
    context = {
        "name": OWNER_NAME,
        "experience_list": objects_from_json(get_experiences_json(request)),
        "title_query": _title_query(request),
    }
    return render(request, "experience.html", context)


def get_projects_json(request):
    """return data Project dalam JSON"""
    return json_response(filter_by_title(Project.objects.all(), _title_query(request)))


def show_project(request):
    """show Project dari JSON yang di deserialize + search"""
    context = {
        "name": OWNER_NAME,
        "project_list": objects_from_json(get_projects_json(request)),
        "title_query": _title_query(request),
    }
    return render(request, "project.html", context)


def show_project_detail(request, slug):
    """halaman detail satu Project based on slug"""
    project = get_object_or_404(Project, slug=slug)
    return render(
        request,
        "project_detail.html",
        {"name": OWNER_NAME, "project": project},
    )


# Admin panel (staff only)

@staff_required
def admin_dashboard(request):
    """dashboard staff kelola Experience & Project + search"""
    q = request.GET.get("q", "").strip()
    context = {
        "name": OWNER_NAME,
        "experience_list": filter_by_title(Experience.objects.order_by("-started_at"), q),
        "project_list": filter_by_title(Project.objects.order_by("title"), q),
        "q": q,
    }
    return render(request, "admin/dashboard.html", context)


@staff_required
def create_experience(request):
    """tambah Experience lewat form"""
    form = ExperienceForm(request.POST or None)
    return _handle_form(request, form, "Add Experience", "Experience berhasil ditambahkan!")


@staff_required
def update_experience(request, experience_id):
    """ubah Experience lewat form"""
    experience = get_object_or_404(Experience, id=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    return _handle_form(request, form, "Edit Experience", "Experience berhasil diperbarui!")


@staff_required
@require_POST
def delete_experience(request, experience_id):
    """hapus Experience cuman lewat POST"""
    experience = get_object_or_404(Experience, id=experience_id)
    return _delete_and_redirect(experience, "Experience berhasil dihapus!", request)


@staff_required
def create_project(request):
    """tambah Project lewat form, slug otomatis dari judul"""
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.slug = unique_slug(project.title)
        project.tech_stack = []
        project.save()
        messages.success(request, "Project berhasil ditambahkan!")
        return redirect("main:admin_dashboard")

    return _admin_form(request, form, "Add Project")


@staff_required
def update_project(request, slug):
    """ubah Project lewat form"""
    project = get_object_or_404(Project, slug=slug)
    form = ProjectForm(request.POST or None, instance=project)
    return _handle_form(request, form, "Edit Project", "Project berhasil diperbarui!")


@staff_required
@require_POST
def delete_project(request, slug):
    """hapus Project lewat POST aja"""
    project = get_object_or_404(Project, slug=slug)
    return _delete_and_redirect(project, "Project berhasil dihapus!", request)
