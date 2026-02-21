from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostsFeed(Feed):
    title = "Latest Blog Posts"
    description = "Updates on the latest posts."

    def link(self):
        return reverse("blog")

    def items(self):
        return Post.published.order_by("-published_at")[:20]

    def item_title(self, item: Post):
        return item.title

    def item_description(self, item: Post):
        return item.excerpt
