from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient

from apps.ai.services import answer_question
from apps.blog.models import Post
from apps.portfolio.models import Project
from me.models import Profile


class AssistantTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.profile = Profile.objects.create(
            name="Muhammadrizo",
            full_name="Muhammadrizo Sultonov",
            role="Backend Developer",
            tagline="Backend",
            bio="Python and Django developer.",
            email="muhammadrizosultonov33@gmail.com",
            phone="+998777920060",
            telegram="@sultonovengineer",
            github="https://github.com/muhammadrizosultonov",
            skills_text="Python, Django, DRF, FastAPI",
        )
        self.project1 = Project.objects.create(
            title="CRM Platform",
            description="CRM for sales teams",
            tech_stack="Django, PostgreSQL",
            year=2025,
        )
        self.project2 = Project.objects.create(
            title="FastAPI Service",
            description="API gateway",
            tech_stack="FastAPI, Redis",
            year=2024,
        )
        Post.objects.create(
            title="Django Tips",
            excerpt="How to structure Django apps",
            content="Test",
            is_published=True,
        )

    def test_contact_question(self):
        result = answer_question("How can I contact you?")
        self.assertIn("Email", result["answer"])
        self.assertIn(self.profile.email, result["answer"])

    def test_project_scoring(self):
        result = answer_question("Tell me about your Django projects")
        project_titles = [item["title"] for item in result["sources"]["projects"]]
        self.assertIn(self.project1.title, project_titles)

    def test_rate_limit(self):
        for _ in range(20):
            response = self.client.post(
                "/api/chat/",
                {"message": "hi"},
                format="json",
                REMOTE_ADDR="10.0.0.1",
            )
            self.assertNotEqual(response.status_code, 429)
        response = self.client.post(
            "/api/chat/",
            {"message": "hi"},
            format="json",
            REMOTE_ADDR="10.0.0.1",
        )
        self.assertEqual(response.status_code, 429)
