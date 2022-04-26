from django.urls import path, re_path
from dargs import views

urlpatterns = [
    path("analysis/1", views.analysis_1),
    path("analysis/2", views.analysis_2),
    path("analysis/3", views.analysis_3),
    path("analysis/4", views.analysis_4),
    path("analysis/5", views.analysis_5),
    path("analysis/6", views.analysis_6),
    path("school", views.SchoolListView.as_view()),
    path("semester", views.SemesterListView.as_view()),
    path("size", views.analysis_range_sizes),
    re_path(r"^upload/(?P<filename>[^/]+)$", views.FileUploadView.as_view()),
    path("clear", views.clear_db),
]
