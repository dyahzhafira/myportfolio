from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, Select, URLInput, DateTimeInput
from django.utils.html import strip_tags

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
            "project_url",
            "project_image_url",
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
            "project_url": URLInput(
                attrs={"placeholder": "https://github.com/username/repo"}
            ),
            "project_image_url": URLInput(
                attrs={"placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000"}
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()


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

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama experience tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()