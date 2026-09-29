from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_project,
    show_project_detail,
    get_projects_json,
    get_projects_data,
    get_experiences_json,
    admin_dashboard,
    create_experience,
    update_experience,
    delete_experience,
    create_project,
    create_project_ajax,
    update_project,
    delete_project,
    register,
    login_user,
    logout_user,
    toggle_star,
    toggle_star_ajax,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("project/", show_project, name="show_project"),
    path("project/<slug:slug>/", show_project_detail, name="show_project_detail"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("api/projects/data/", get_projects_data, name="get_projects_data"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path(
        "project/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
    path(
        "project/<uuid:project_id>/star-ajax/",
        toggle_star_ajax,
        name="toggle_star_ajax",
    ),
    path("project/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("admin-panel/", admin_dashboard, name="admin_dashboard"),
    path("admin-panel/experiences/add/", create_experience, name="create_experience"),
    path(
        "admin-panel/experiences/<uuid:experience_id>/edit/",
        update_experience,
        name="update_experience",
    ),
    path(
        "admin-panel/experiences/<uuid:experience_id>/delete/",
        delete_experience,
        name="delete_experience",
    ),
    path("admin-panel/projects/add/", create_project, name="create_project"),
    path(
        "admin-panel/projects/<slug:slug>/edit/",
        update_project,
        name="update_project",
    ),
    path(
        "admin-panel/projects/<slug:slug>/delete/",
        delete_project,
        name="delete_project",
    ),
]
