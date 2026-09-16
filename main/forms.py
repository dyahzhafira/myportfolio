from django.forms import ModelForm, TextInput, Textarea, Select, URLInput

from main.models import Project

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
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "status": "Status",
            "project_type": "Tipe Proyek",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
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
                    "placeholder": "Ceritakan proyekmu",
                    "rows": 3,
                }
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
