from django.urls import path

from reports import views


urlpatterns = [
    path(
        "users/",
        views.UserReportView.as_view(),
        name="users",
    ),
]
