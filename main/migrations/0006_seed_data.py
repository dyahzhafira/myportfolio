from django.db import migrations
from django.utils import timezone
import datetime


def seed_data(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")
    Project = apps.get_model("main", "Project")

    tz = timezone.get_current_timezone()

    experiences = [
        {
            "title": "Teaching Assistant of Discrete Math I",
            "description": "Faculty of Computer Science, Universitas Indonesia. Deliver tutoring sessions and assist undergraduate students in core discrete mathematics concepts. Develop practice problems and grade submissions, providing feedback to reinforce understanding.",
            "category": "part-time",
            "started_at": datetime.datetime(2026, 8, 1, tzinfo=tz),
            "ended_at": None,
        },
        {
            "title": "Software Engineer Academy Staff",
            "description": "COMPFEST. Recruited & coordinated mentors, speakers, and judges for the Software Engineer Academy Program. Conducted participant selection through assignment assessments and interviews. Served as MC during program sessions and events.",
            "category": "volunteer",
            "started_at": datetime.datetime(2026, 4, 1, tzinfo=tz),
            "ended_at": None,
        },
        {
            "title": "Developer",
            "description": "Badan Eksekutif Mahasiswa Universitas Indonesia (BEM UI). Developed & maintained web platforms for BEM UI's open recruitments and event registrations. Designed UI/UX prototypes and interfaces for BEM UI website. Assisted the publication team in managing digital publications.",
            "category": "volunteer",
            "started_at": datetime.datetime(2026, 3, 1, tzinfo=tz),
            "ended_at": None,
        },
        {
            "title": "Data and Technology Associate",
            "description": "StudentsxCEOs Jakarta. Developed and maintained the organization's external website with a focus on scalability and usability to support better information access. Implemented updates and managed content to ensure accurate and real time information delivery. Collaborated with multiple divisions to translate operational needs into functional web features.",
            "category": "part-time",
            "started_at": datetime.datetime(2026, 2, 1, tzinfo=tz),
            "ended_at": None,
        },
        {
            "title": "Web Developer",
            "description": "BETIS Fasilkom UI. Developed and maintained responsive front-end components for the event website. Collaborated with back-end and UI/UX teams to ensure seamless API integration and consistent user interface. Contributed to building a functional and user-friendly website to support event operations.",
            "category": "volunteer",
            "started_at": datetime.datetime(2026, 1, 1, tzinfo=tz),
            "ended_at": datetime.datetime(2026, 4, 30, tzinfo=tz),
        },
    ]

    for data in experiences:
        Experience.objects.get_or_create(title=data["title"], defaults=data)

    projects = [
        {
            "title": "SignD - Disaster Response Platform for Disabilities",
            "slug": "signd",
            "description": "Platform respons bencana end-to-end yang dirancang agar bantuan darurat lebih mudah diakses oleh penyandang disabilitas sensorik, dari riset awal hingga arsitektur sistem dan produk yang siap dipakai.",
            "status": "progress",
            "project_type": "individual",
            "tech_stack": [
                {"name": "Flutter", "icon": "flutter"},
                {"name": "Go/Fiber", "icon": "go"},
                {"name": "Python/FastAPI", "icon": "fastapi"},
                {"name": "PostgreSQL", "icon": "postgresql"},
            ],
        },
        {
            "title": "BEM UI - Sistem Perekrutan Terbuka",
            "slug": "bem-ui-spt",
            "description": "Platform perekrutan dan registrasi acara terpusat untuk BEM UI, terintegrasi SSO kampus, dipakai di 10+ program dengan 100-500+ pendaftar tiap program.",
            "status": "completed",
            "project_type": "group",
            "tech_stack": [
                {"name": "Next.js", "icon": "nextdotjs"},
                {"name": "Bun/Hono", "icon": "bun"},
                {"name": "TypeScript", "icon": "typescript"},
            ],
        },
        {
            "title": "ClinicThinking - AI Clinical Reasoning Simulation",
            "slug": "clinicthinking",
            "description": "Platform simulasi klinis berbasis AI yang mendeteksi pola bias kognitif dari cara pengguna mengambil keputusan langkah demi langkah, bukan cuma menilai jawaban akhirnya.",
            "status": "progress",
            "project_type": "group",
            "tech_stack": [
                {"name": "Go/Fiber", "icon": "go"},
                {"name": "Python/FastAPI", "icon": "fastapi"},
                {"name": "Gemini API", "icon": "googlegemini"},
            ],
        },
    ]

    for data in projects:
        Project.objects.get_or_create(slug=data["slug"], defaults=data)


def remove_data(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")
    Project = apps.get_model("main", "Project")
    Experience.objects.filter(
        title__in=[
            "Teaching Assistant of Discrete Math I",
            "Software Engineer Academy Staff",
            "Developer",
            "Data and Technology Associate",
            "Web Developer",
        ]
    ).delete()
    Project.objects.filter(slug__in=["signd", "bem-ui-spt", "clinicthinking"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_alter_project_slug"),
    ]

    operations = [
        migrations.RunPython(seed_data, remove_data),
    ]
