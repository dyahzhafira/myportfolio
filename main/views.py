import datetime
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project
from main.services import filter_by_title, json_response, unique_slug

OWNER_NAME = "Dyah Zhafira"


def role_required(check):
    """Factory decorator"""

    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url="/login/")
        def wrapper(request, *args, **kwargs):
            if not check(request.user):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

owner_required = role_required(lambda user: user.is_superuser)
editor_or_owner_required = role_required(
    lambda user: user.is_superuser or user.groups.filter(name="Editor").exists()
)


def _title_query(request):
    """ambil keyword title dari query string."""
    return request.GET.get("title", "").strip()

def _is_editor(request):
    return request.user.is_authenticated and request.user.groups.filter(name="Editor").exists()


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
    last_login = request.COOKIES.get(
        "last_login", "Belum ada sesi login / Cookie tidak ditemukan"
    )
    context = {
        "last_login": last_login,
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


def get_experiences_data(request):
    """return data Experience dalam JSON buat AJAX render"""
    experiences = filter_by_title(
        Experience.objects.prefetch_related("starred_by").order_by("-started_at"),
        _title_query(request),
    )

    data = []
    for experience in experiences:
        starred_users = experience.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        data.append(
            {
                "id": str(experience.id),
                "fields": {
                    "title": experience.title,
                    "description": experience.description,
                    "category_display": experience.get_category_display(),
                    "is_ongoing": experience.is_ongoing,
                    "thumbnail": experience.thumbnail,
                    "star_count": starred_users.count(),
                    "is_starred": is_starred,
                    "starred_by_names": ", ".join(u.username for u in starred_users),
                },
            }
        )

    return JsonResponse(data, safe=False)


@ensure_csrf_cookie
def show_experience(request):
    """render kerangka halaman Experience"""
    context = {
        "name": OWNER_NAME,
        "title_query": _title_query(request),
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)


def get_projects_json(request):
    """return data Project dalam JSON, tanpa daftar user yang nge-star"""
    return json_response(
        filter_by_title(Project.objects.all(), _title_query(request)),
        exclude=["starred_by"],
    )


def get_projects_data(request):
    """return data Project dalam JSON buat AJAX render"""
    projects = filter_by_title(Project.objects.prefetch_related("starred_by"), _title_query(request))

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        data.append(
            {
                "id": str(project.id),
                "slug": project.slug,
                "fields": {
                    "title": project.title,
                    "description": project.description,
                    "status_display": project.get_status_display(),
                    "project_type_display": project.get_project_type_display(),
                    "tech_stack": project.tech_stack,
                    "project_url": project.project_url,
                    "project_image_url": project.project_image_url,
                    "star_count": starred_users.count(),
                    "is_starred": is_starred,
                    "starred_by_names": ", ".join(u.username for u in starred_users),
                },
            }
        )

    if request.GET.get("sort", "") == "star":
        data.sort(key=lambda item: item["fields"]["star_count"], reverse=True)

    return JsonResponse(data, safe=False)


@ensure_csrf_cookie
def show_project(request):
    """render kerangka halaman Project, data proyek diambil lewat AJAX oleh client"""
    context = {
        "name": OWNER_NAME,
        "title_query": _title_query(request),
        "sort_by": request.GET.get("sort", ""),
        "is_editor": _is_editor(request),
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)


def show_project_detail(request, slug):
    """halaman detail satu Project based on slug"""
    project = get_object_or_404(Project, slug=slug)
    return render(
        request,
        "project_detail.html",
        {"name": OWNER_NAME, "project": project, "is_editor": _is_editor(request)},
    )


# Auth

def register(request):
    """daftar akun baru pakai UserCreationForm"""
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    return render(request, "register.html", {"name": OWNER_NAME, "form": form})


def login_user(request):
    """login + set cookie last_login"""
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie(
            "last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return response

    return render(request, "login.html", {"name": OWNER_NAME, "form": form})


@require_POST
def logout_user(request):
    """logout + hapus cookie last_login"""
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


# Star (semua akun yang login)

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    """beri/batalkan star pada Project, hanya lewat POST"""
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_project")


@require_POST
def toggle_star_ajax(request, project_id):
    """kasih/batalin star pada Project lewat AJAX.

    Sengaja tidak pakai @login_required di sini karena dekorator itu akan
    redirect ke halaman login (status 200, bukan 403) kalau belum login, dan
    fetch() di frontend akan mengikuti redirect itu lalu menerima HTML
    halaman login tanpa tahu permintaannya sebenarnya ditolak. Cek manual
    di bawah memastikan AJAX selalu dapat JSON 403 yang jelas.
    """
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Silakan login terlebih dahulu untuk memberi star."}, status=403
        )

    project = get_object_or_404(Project, pk=project_id)

    if request.user in project.starred_by.all():
        project.starred_by.remove(request.user)
        is_starred = False
        message = "Star dibatalkan."
    else:
        project.starred_by.add(request.user)
        is_starred = True
        message = "Project berhasil diberi star."

    return JsonResponse(
        {
            "message": message,
            "is_starred": is_starred,
            "star_count": project.starred_by.count(),
        }
    )


@require_POST
def toggle_experience_star_ajax(request, experience_id):
    """kasih/batalin star pada Experience lewat AJAX.

    Sama kayak toggle_star_ajax: pakai cek manual, bukan @login_required,
    biar pengunjung yang belum login dapat JSON 403 yang jelas lewat fetch(),
    bukan ikut redirect ke halaman login.
    """
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Silakan login terlebih dahulu untuk memberi star."}, status=403
        )

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.user in experience.starred_by.all():
        experience.starred_by.remove(request.user)
        is_starred = False
        message = "Star dibatalkan."
    else:
        experience.starred_by.add(request.user)
        is_starred = True
        message = "Experience berhasil diberi star."

    return JsonResponse(
        {
            "message": message,
            "is_starred": is_starred,
            "star_count": experience.starred_by.count(),
        }
    )


# Admin panel (owner/superuser only)

@editor_or_owner_required
def admin_dashboard(request):
    """dashboard owner kelola Experience & Project + search"""
    q = request.GET.get("q", "").strip()
    context = {
        "name": OWNER_NAME,
        "experience_list": filter_by_title(Experience.objects.order_by("-started_at"), q),
        "project_list": filter_by_title(Project.objects.order_by("title"), q),
        "q": q,
        "is_editor": _is_editor(request),
    }
    return render(request, "admin/dashboard.html", context)


@owner_required
def create_experience(request):
    """tambah Experience lewat form"""
    form = ExperienceForm(request.POST or None)
    return _handle_form(request, form, "Add Experience", "Experience berhasil ditambahkan!")


@require_POST
def create_experience_ajax(request):
    """tambah Experience lewat AJAX dari modal di halaman /experience/.

    Sama kayak create_project_ajax: permission dicek manual di dalam view,
    bukan cuma disembunyikan di template, dan validasi tetap lewat
    ExperienceForm yang sama dengan form create biasa.
    """
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya owner yang dapat menambahkan experience."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "id": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@owner_required
def update_experience(request, experience_id):
    """ubah Experience lewat form"""
    experience = get_object_or_404(Experience, id=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    return _handle_form(request, form, "Edit Experience", "Experience berhasil diperbarui!")


@owner_required
@require_POST
def delete_experience(request, experience_id):
    """hapus Experience cuman lewat POST"""
    experience = get_object_or_404(Experience, id=experience_id)
    return _delete_and_redirect(experience, "Experience berhasil dihapus!", request)


@owner_required
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


@require_POST
def create_project_ajax(request):
    """tambah Project lewat AJAX dari modal di halaman /project/.

    Permission dicek manual di sini (bukan cuma disembunyikan di template),
    karena menyembunyikan tombol modal tidak mencegah siapa pun memanggil
    endpoint ini langsung lewat fetch() atau curl. Validasi tetap lewat
    ProjectForm yang sama dengan form create biasa, termasuk clean_title
    dan clean_description yang membersihkan tag HTML.
    """
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya owner yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save(commit=False)
        project.slug = unique_slug(project.title)
        project.tech_stack = []
        project.save()
        return JsonResponse(
            {"message": "Project berhasil ditambahkan.", "slug": project.slug},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@editor_or_owner_required
def update_project(request, slug):
    """ubah Project lewat form"""
    project = get_object_or_404(Project, slug=slug)
    form = ProjectForm(request.POST or None, instance=project)
    return _handle_form(request, form, "Edit Project", "Project berhasil diperbarui!")


@owner_required
@require_POST
def delete_project(request, slug):
    """hapus Project lewat POST aja"""
    project = get_object_or_404(Project, slug=slug)
    return _delete_and_redirect(project, "Project berhasil dihapus!", request)
