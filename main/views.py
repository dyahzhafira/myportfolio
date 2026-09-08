from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Dyah Zhafira Wibowo",
        "npm": "2506623723",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Hi, I'm Dyah! Let's get to know each other :)"
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Dyah Zhafira",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)