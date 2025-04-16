from django.shortcuts import render

from newspaper.models import Advertisement, Category, Post, Tag
from django.views.generic import ListView

from django.utils import timezone
from datetime import timedelta


class SidebarMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["popular_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:5]

        context["advertisement"] = (
            Advertisement.objects.all().order_by("-created_at").first()
        )

        return context


class HomeView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-published_at")[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )

        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago
        ).order_by("-published_at", "-views_count")[:5]

        return context


class PostListView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")


class PostByCategoryView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            category__id=self.kwargs["category_id"],
        ).order_by("-published_at")
        return query


class TagListView(ListView):
    model = Tag
    template_name = "newsportal/tags.html"
    context_object_name = "tags"
