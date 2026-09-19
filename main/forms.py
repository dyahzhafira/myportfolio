from django.forms import ModelForm, TextInput, Textarea, Select, URLInput, DateTimeInput

from main.models import Project, Experience

DATETIME_LOCAL = "%Y-%m-%dT%H:%M"


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "status",
            "project_type",
        ]

        labels = {
            "title": "Project's name",
            "description": "Project's description",
            "status": "Status",
            "project_type": "Project's type",
        }

        widgets = {
            "title": TextInput(
                attrs={"placeholder": "Portfolio Website", "maxlength": 255}
            ),
            "description": Textarea(
                attrs={"placeholder": "Tell us ur project here...", "rows": 3}
            ),
            "status": Select(),
            "project_type": Select(),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]
        labels = {
            "title": "Experience's name",
            "description": "Experience's description",
            "category": "Experience's category",
            "thumbnail": "URL Thumbnail",
            "started_at": "Start",
            "ended_at": "End",
        }

        widgets = {
            "title": TextInput(
                attrs={"placeholder": "Your experience's name here...", "maxlength": 255}
            ),
            "description": Textarea(
                attrs={"placeholder": "Tell us ur experience here...", "rows": 4}
            ),
            "category": Select(),
            "thumbnail": URLInput(attrs={"placeholder": "https://example.com/image.jpg"}),
            "started_at": DateTimeInput(
                format=DATETIME_LOCAL, attrs={"type": "datetime-local"}
            ),
            "ended_at": DateTimeInput(
                format=DATETIME_LOCAL, attrs={"type": "datetime-local"}
            ),
        }
