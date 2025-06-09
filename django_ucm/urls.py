from django.contrib import admin
from django.urls import path

from portal import views
from portal.views import EvaluationEditView, EvaluationUpdateView, EvaluationByCourseView, EvaluationDeleteById

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('evaluations/', EvaluationEditView.as_view(), name='evaluations-edit'),
    path('evaluations/edit', EvaluationUpdateView.as_view(), name='evaluations-update'),
    path('evaluations/<str:course_id>/', EvaluationByCourseView.as_view(), name='evaluations-by-course'),
    path('evaluations/<uuid:id>', EvaluationDeleteById.as_view(), name='evaluation-delete')

]


