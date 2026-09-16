from django.urls import path

from main.views import show_main, show_experience, show_project, show_project_detail, create_project, delete_project, get_projects_json

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("project/", show_project,name="show_project"),
    path("project/<slug:slug>/", show_project_detail, name="show_project_detail"),
    path("projects/add/", create_project, name="create_project"),
    path("project/<slug:slug>/delete/",delete_project, name="delete_project"),
    path("api/projects/", get_projects_json,name="get_projects_json"),
]