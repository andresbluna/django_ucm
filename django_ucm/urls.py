from django.contrib import admin
from django.urls import path

from portal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('evaluations', views.evaluation_create_update, name='evaluation_create_update'),  # POST y PUT

    # GET evaluaciones por curso:
    path('evaluations/course/<str:course_id>/', views.evaluation_list_by_course, name='evaluation_list_by_course'),

    # DELETE evaluación por id:
    path('evaluations/delete/<str:id>/', views.evaluation_delete, name='evaluation_delete'),

    path('external-cursos/', views.external_courses_api, name='external_courses_api')
]


