from django.contrib import admin
from django.urls import path

from portal import views
from portal.views import EvaluationListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('evaluations/', EvaluationListView.as_view(), name='evaluations'),
]


