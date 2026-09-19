from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at="2026-01-01",
        )

        self.project = Project.objects.create(
            title="SignD",
            slug="signd-test",
            description="Platform Siaga Bencana Inklusif untuk Disabilitas",
            status="progress",
            project_type="individual",
            tech_stack=[
                {
                    "name":"Go/Fiber",
                    "icon":"go",
                },
                {
                    "name": "Flutter",
                    "icon": "flutter",
                }
            ]
        )
        
        Experience.objects.exclude(pk=self.experience.pk).delete()
        Project.objects.exclude(pk=self.project.pk).delete()

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_project_page(self):
        response = self.client.get(reverse("main:show_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "In Progress")
        self.assertContains(response, "Individual")


    def test_project_data_is_displayed(self):
        response = self.client.get(reverse("main:show_project"))
        self.assertContains(response, "SignD")
        self.assertContains(response, "Go/Fiber")


    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_project"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_project_detail_page(self):
        response = self.client.get(reverse("main:show_project_detail", args=[self.project.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_detail.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "In Progress")
        self.assertContains(response, "Individual")

    def test_project_detail_not_found(self):
        response = self.client.get(reverse("main:show_project_detail", args=["slug-yang-gak-ada"]))

        self.assertEqual(response.status_code, 404)

class ExperienceAdminTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="test_admin",
            password="test_password_123",
            is_staff=True,
        )

        self.experience = Experience.objects.create(
            title="Test Experience",
            description="Test description",
            category="research",
            started_at="2026-01-01T09:00:00Z",
            ended_at=None,
        )

    def test_admin_dashboard_requires_login(self):
        response = self.client.get(
            reverse("main:admin_dashboard")
        )

        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_accessible_for_staff(self):
        self.client.login(
            username="test_admin",
            password="test_password_123",
        )

        response = self.client.get(
            reverse("main:admin_dashboard")
        )

        self.assertEqual(response.status_code, 200)

    def test_create_experience(self):
        self.client.login(
            username="test_admin",
            password="test_password_123",
        )

        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "New Experience",
                "description": "New description",
                "category": "internship",
                "thumbnail": "",
                "started_at": "2026-02-01T09:00",
                "ended_at": "",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Experience.objects.filter(
                title="New Experience"
            ).exists()
        )

    def test_update_experience(self):
        self.client.login(
            username="test_admin",
            password="test_password_123",
        )

        response = self.client.post(
            reverse(
                "main:update_experience",
                args=[self.experience.id],
            ),
            {
                "title": "Updated Experience",
                "description": "Updated description",
                "category": "research",
                "thumbnail": "",
                "started_at": "2026-01-01T09:00",
                "ended_at": "",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Updated Experience",
        )

    def test_delete_experience(self):
        self.client.login(
            username="test_admin",
            password="test_password_123",
        )

        response = self.client.post(
            reverse(
                "main:delete_experience",
                args=[self.experience.id],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Experience.objects.filter(
                id=self.experience.id
            ).exists()
        )

    def test_experience_json(self):
        response = self.client.get(
            reverse("main:get_experiences_json")
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response["Content-Type"],
            "application/json",
        )