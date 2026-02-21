import re
from typing import List

from apps.blog.models import Post
from apps.portfolio.models import Project
from me.models import Profile


def tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-zA-Z0-9]+", (text or "").lower()) if len(t) > 2]


def score_text(text: str, query_tokens: List[str]) -> float:
    if not text or not query_tokens:
        return 0.0
    tokens = set(tokenize(text))
    if not tokens:
        return 0.0
    overlap = len(tokens.intersection(query_tokens))
    return overlap / max(len(tokens), 1)


def top_projects(query: str, limit: int = 2) -> List[Project]:
    tokens = tokenize(query)
    projects = list(Project.objects.all())
    scored = [
        (score_text(f"{p.title} {p.description} {p.tech_stack}", tokens), p)
        for p in projects
    ]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for score, p in scored[:limit] if score > 0] or projects[:limit]


def top_posts(query: str, limit: int = 2) -> List[Post]:
    tokens = tokenize(query)
    posts = list(Post.published.all())
    scored = [
        (score_text(f"{p.title} {p.excerpt}", tokens), p)
        for p in posts
    ]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for score, p in scored[:limit] if score > 0] or posts[:limit]


def build_context_text(query: str) -> str:
    profile = Profile.objects.first()
    projects = top_projects(query)
    posts = top_posts(query)

    lines = []
    if profile:
        age_text = ""
        if profile.date_of_birth:
            from datetime import date

            today = date.today()
            years = today.year - profile.date_of_birth.year
            if (today.month, today.day) < (
                profile.date_of_birth.month,
                profile.date_of_birth.day,
            ):
                years -= 1
            age_text = f"- Age: {years}"

        lines.append("Profile:")
        lines.append(f"- Name: {profile.full_name or profile.name}")
        lines.append(f"- Role: {profile.role}")
        lines.append(f"- Bio: {profile.bio}")
        lines.append(f"- Location: {profile.location}")
        lines.append(f"- Email: {profile.email}")
        lines.append(f"- Phone: {profile.phone}")
        lines.append(f"- Telegram: {profile.telegram}")
        lines.append(f"- GitHub: {profile.github}")
        lines.append(f"- Skills: {profile.skills_text}")
        if age_text:
            lines.append(age_text)

    lines.append("Projects:")
    for project in projects:
        lines.append(
            f"- {project.title}: {project.description} | Tech: {project.tech_stack}"
        )

    lines.append("BlogPosts:")
    for post in posts:
        lines.append(f"- {post.title}: {post.excerpt}")

    return "\n".join(lines)
