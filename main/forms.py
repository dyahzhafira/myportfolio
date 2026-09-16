from django.forms import ModelForm, TextInput, Textarea, Select

from main.models import Project

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
            "title": "Nama Project",
            "description": "Deskripsi Project",
            "status": "Status",
            "project_type": "Tipe Project",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell us ur project here...",
                    "rows": 3,
                }
            ),
            "status": Select(),
            "project_type": Select(),
        }
