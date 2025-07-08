from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, View

from dashboard.forms import CategoryForm, PostForm, TagForm
from newspaper.models import Category, Post, Tag


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("/")


# Create your views here.
class AdminPostListView(StaffRequiredMixin, ListView):
    model = Post
    template_name = "dashboard/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.all().order_by("-published_at")


class AdminPostCreateView(StaffRequiredMixin, CreateView):
    model = Post
    template_name = "dashboard/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("admin-post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdminDraftPublishView(StaffRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk, published_at__isnull=True)
        post.published_at = timezone.now()
        post.save()
        return redirect("admin-post-list")


class AdminPostDeleteView(StaffRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("admin-post-list")


class AdminPostUpdateView(StaffRequiredMixin, UpdateView):
    model = Post
    template_name = "dashboard/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("admin-post-list")


######### Tag


class AdminTagListView(StaffRequiredMixin, ListView):
    model = Tag
    template_name = "dashboard/tag_list.html"
    context_object_name = "tags"

    def get_queryset(self):
        return Tag.objects.all()


class AdminTagCreateView(StaffRequiredMixin, CreateView):
    model = Tag
    template_name = "dashboard/tag_create.html"
    form_class = TagForm
    success_url = reverse_lazy("admin-tag-list")


class AdminTagDeleteView(StaffRequiredMixin, View):
    def get(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return redirect("admin-tag-list")


class AdminTagUpdateView(StaffRequiredMixin, UpdateView):
    model = Tag
    template_name = "dashboard/tag_create.html"
    form_class = TagForm
    success_url = reverse_lazy("admin-tag-list")


######### Category


class AdminCategoryListView(StaffRequiredMixin, ListView):
    model = Category
    template_name = "dashboard/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.all()


class AdminCategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    template_name = "dashboard/category_create.html"
    form_class = CategoryForm
    success_url = reverse_lazy("admin-category-list")


class AdminCategoryDeleteView(StaffRequiredMixin, View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return redirect("admin-category-list")


class AdminCategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    template_name = "dashboard/category_create.html"
    form_class = CategoryForm
    success_url = reverse_lazy("admin-category-list")
