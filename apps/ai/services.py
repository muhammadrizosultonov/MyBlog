import re
from dataclasses import dataclass
from typing import List

from apps.blog.models import Post
from apps.portfolio.models import Project
from me.models import Profile


@dataclass
class ScoredItem:
    id: int
    title: str
    text: str
    score: float


def _tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-zA-Z0-9]+", (text or "").lower()) if len(t) > 2]


def _score(text: str, query_tokens: List[str]) -> float:
    if not text or not query_tokens:
        return 0.0
    content_tokens = set(_tokenize(text))
    if not content_tokens:
        return 0.0
    overlap = len(content_tokens.intersection(query_tokens))
    return overlap / max(len(content_tokens), 1)


def _top_items(items: List[ScoredItem], limit: int = 3) -> List[ScoredItem]:
    return sorted(items, key=lambda item: item.score, reverse=True)[:limit]


def _skills_summary(profile: Profile) -> str:
    if not profile:
        return ""
    if profile.skills_text:
        return profile.skills_text
    skills = list(profile.skills.values_list("name", flat=True))
    return ", ".join(skills)


def _contact_summary(profile: Profile) -> str:
    if not profile:
        return "Contact info is not available yet."
    parts = []
    if profile.email:
        parts.append(f"Email: {profile.email}")
    if profile.phone:
        parts.append(f"Phone: {profile.phone}")
    if profile.telegram:
        parts.append(f"Telegram: {profile.telegram}")
    if profile.github:
        parts.append(f"GitHub: {profile.github}")
    if not parts:
        return "Contact info is not available yet."
    return " | ".join(parts)


def answer_question(message: str) -> dict:
    profile = Profile.objects.first()
    query_tokens = _tokenize(message)

    projects = list(Project.objects.all())
    project_items = [
        ScoredItem(
            id=project.id,
            title=project.title,
            text=f"{project.title} {project.description} {project.tech_stack}",
            score=_score(f"{project.title} {project.description} {project.tech_stack}", query_tokens),
        )
        for project in projects
    ]

    posts = list(Post.published.all())
    post_items = [
        ScoredItem(
            id=post.id,
            title=post.title,
            text=f"{post.title} {post.excerpt}",
            score=_score(f"{post.title} {post.excerpt}", query_tokens),
        )
        for post in posts
    ]

    top_projects = _top_items(project_items)
    top_posts = _top_items(post_items)

    message_l = message.lower()
    is_contact = any(k in message_l for k in ["contact", "email", "phone", "telegram", "github", "reach"])
    is_skills = any(k in message_l for k in ["skill", "stack", "tech", "technology", "framework"])
    is_projects = any(k in message_l for k in ["project", "portfolio", "work", "case"])
    is_blog = any(k in message_l for k in ["blog", "post", "article", "write", "writing"])

    if is_contact:
        answer = _contact_summary(profile)
    elif is_skills:
        skills_text = _skills_summary(profile)
        if skills_text:
            answer = f"Primary skills: {skills_text}."
        else:
            answer = "Skills information is not available yet."
    elif is_projects:
        if top_projects:
            lines = ["Here are relevant projects:"]
            for item in top_projects:
                project = next((p for p in projects if p.id == item.id), None)
                if project:
                    lines.append(f"- {project.title}: {project.description}")
            answer = "\n".join(lines)
        else:
            answer = "No projects are available yet."
    elif is_blog:
        if top_posts:
            lines = ["Here are relevant posts:"]
            for item in top_posts:
                post = next((p for p in posts if p.id == item.id), None)
                if post:
                    lines.append(f"- {post.title}: {post.excerpt}")
            answer = "\n".join(lines)
        else:
            answer = "No blog posts are available yet."
    else:
        if profile:
            name = profile.full_name or profile.name
            answer = (
                f"I am {name}, {profile.role}. {profile.bio or ''} "
                "You can ask about my skills, projects, blog posts, or contact details."
            ).strip()
        else:
            answer = "Profile information is not available yet."

    sources = {
        "projects": [
            {"title": p.title, "id": p.id}
            for p in projects
            if p.id in [i.id for i in top_projects]
        ],
        "posts": [
            {"title": p.title, "id": p.id}
            for p in posts
            if p.id in [i.id for i in top_posts]
        ],
    }

    return {"answer": answer, "sources": sources}
