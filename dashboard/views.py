from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import EmailMultiAlternatives, get_connection
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, View

from dashboard.forms import CategoryForm, PostForm, TagForm
from newspaper.models import Category, Newsletter, Post, Tag


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

    def send_newsletter_email(self, post, request):
        subscribers = Newsletter.objects.all()

        if subscribers.exists():
            messages = []
            subject = f"New Post Published: {post.title}"
            from_email = settings.DEFAULT_FROM_EMAIL

            for subscriber in subscribers:
                post_url = request.build_absolute_uri(
                    reverse("post-detail", args=[post.pk])
                )
                unsubscribe_url = request.build_absolute_uri(
                    reverse("newsletter-unsubscribe") + f"?email={subscriber.email}"
                )

                context = {
                    "post": post,
                    "post_url": post_url,
                    "unsubscribe_url": unsubscribe_url,
                }

                html_content = render_to_string(
                    "email/new_post_newsletter.html", context
                )
                msg = EmailMultiAlternatives(
                    subject, "", from_email, [subscriber.email]
                )
                msg.attach_alternative(html_content, "text/html")
                messages.append(msg)

            try:
                with get_connection() as connection:
                    connection.send_messages(messages)
            except Exception as e:
                # Log error or handle as needed
                pass

    def get(self, request, pk):
        post = Post.objects.get(pk=pk, published_at__isnull=True)
        post.published_at = timezone.now()
        post.save()
        self.send_newsletter_email(post, request)
        return redirect("admin-post-list")


@method_decorator(csrf_exempt, name="dispatch")
class NewsletterUnsubscribeView(View):
    def get(self, request):
        email = request.GET.get("email")
        if email:
            try:
                subscriber = Newsletter.objects.get(email=email)
                subscriber.delete()
                return HttpResponse("You have been unsubscribed from the newsletter.")
            except Newsletter.DoesNotExist:
                return HttpResponse("Email not found in our subscription list.")
        return HttpResponse("Invalid unsubscribe request.")


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
