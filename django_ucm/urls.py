from django.contrib import admin
from django.urls import path
from portal.views import RegisterFileView
from portal import views
from portal.views import EvaluationEditView, EvaluationUpdateView, EvaluationByCourseView, FilesByCourseQueryView, UpdateFileNameView, DeleteFileView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('evaluations/', EvaluationEditView.as_view(), name='evaluations-edit'),
    path('evaluations/edit', EvaluationUpdateView.as_view(), name='evaluations-update'),
    path('evaluations/<str:course_id>/', EvaluationByCourseView.as_view(), name='evaluations-by-course'),
    path('files/register/', RegisterFileView.as_view(), name='register-file'),
    path('files/by-course/', FilesByCourseQueryView.as_view(), name='files-by-course-query'),
    path('files/<str:file_id>/update-filename/', UpdateFileNameView.as_view(), name='update-file-filename'),
    path('files/<str:file_id>/delete/', DeleteFileView.as_view(), name='delete-file'),
]




