import logging
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from apps.blog.models import Category, Post, Tag
from apps.portfolio.models import Project, ProjectCategory
from .forms import ContactForm
from django.utils.translation import gettext as _
from .models import ContactMessage, Profile

logger = logging.getLogger(__name__)


def home_view(request):
    profile = Profile.objects.first()
    featured_projects = Project.objects.filter(featured=True).order_by("-year")[:6]
    latest_posts = Post.published.order_by("-published_at")[:4]
    stats = profile.stats.all() if profile else []

    context = {
        "profile": profile,
        "featured_projects": featured_projects,
        "latest_posts": latest_posts,
        "stats": stats,
    }
    return render(request, "pages/home.html", context)


def about_view(request):
    profile = Profile.objects.first()
    skills = profile.skills.all() if profile else []
    timeline = profile.timeline.all() if profile else []
    context = {"profile": profile, "skills": skills, "timeline": timeline}
    return render(request, "pages/about.html", context)


@require_http_methods(["GET", "POST"])
def contact_view(request):
    profile = Profile.objects.first()
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if not form.is_honeypot_triggered():
            ip_address = _get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "")[:255]
            cleaned = form.cleaned_data
            contact_message = ContactMessage.objects.create(
                name=cleaned["full_name"],
                email=cleaned["email"],
                subject=cleaned.get("subject", ""),
                message=cleaned["message"],
                ip_address=ip_address,
                user_agent=user_agent,
            )
            email_sent = _send_contact_email(contact_message)
        else:
            email_sent = False
        if email_sent:
            messages.success(request, _("Thanks! I'll reply within 24-48 hours."))
        else:
            messages.success(
                request,
                _("Thanks! Your message was saved. Email notification is temporarily unavailable."),
            )
        return redirect("contact")

    return render(request, "pages/contact.html", {"profile": profile, "form": form})


def _get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _send_contact_email(contact_message: ContactMessage) -> bool:
    subject = f"New contact message from {contact_message.name}"
    body = (
        f"Name: {contact_message.name}\n"
        f"Email: {contact_message.email}\n"
        f"Subject: {contact_message.subject or '—'}\n\n"
        f"Message:\n{contact_message.message}\n\n"
        f"IP: {contact_message.ip_address or '—'}\n"
        f"User Agent: {contact_message.user_agent or '—'}"
    )
    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_TO_EMAIL],
            reply_to=[contact_message.email],
        )
        email.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("Failed to send contact email notification.")
        return False


def projects_view(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    projects = Project.objects.all()
    if query:
        projects = projects.filter(title__icontains=query)
    if category:
        projects = projects.filter(category__slug=category)

    paginator = Paginator(projects.order_by("-year"), 12)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "projects": page,
        "query": query,
        "category": category,
        "categories": ProjectCategory.objects.all(),
    }
    return render(request, "pages/projects.html", context)


def project_detail_view(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related("images"), slug=slug)
    return render(request, "pages/project_detail.html", {"project": project})


def blog_view(request):
    query = request.GET.get("q", "").strip()
    tag = request.GET.get("tag", "").strip()
    category = request.GET.get("category", "").strip()

    posts = Post.published.all()
    if query:
        posts = posts.filter(title__icontains=query)
    if tag:
        posts = posts.filter(tags__slug=tag)
    if category:
        posts = posts.filter(category__slug=category)

    paginator = Paginator(posts.distinct().order_by("-published_at"), 8)
    page = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "pages/blog.html",
        {
            "posts": page,
            "query": query,
            "tag": tag,
            "category": category,
            "categories": Category.objects.all(),
            "tags": Tag.objects.all(),
        },
    )


def blog_detail_view(request, slug):
    post = get_object_or_404(Post.published, slug=slug)
    html, toc = post.render_markdown()
    return render(
        request,
        "pages/blog_detail.html",
        {"post": post, "content_html": html, "toc": toc},
    )
