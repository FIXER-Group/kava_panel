from django.urls import path
from panel import views
from .models import loop_logs
from django_simple_task import defer
from django.contrib.auth.forms import AdminPasswordChangeForm
import datetime



app_name="panel"
urlpatterns = [
    path('', views.index, name='index'),
    path('process/', views.process, name='process'),
    path('network/', views.network, name='network'),
    path('logout/', views.logout_view, name='logout'),
    path('system/', views.system, name='system'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('webs/', views.webs, name='webs'),
    path('json/chartcpu', views.LineChartCpu.as_view(), name='chartcpu'),
    path('json/chartram', views.LineChartRam.as_view(), name='chartram'),
    path('json/stats_update', views.stats_update, name='stats_update'),
    path('api/stats', views.StatsAPIView.as_view(), name='statsapi'),
    path('api/system', views.SystemAPIView.as_view(), name='systemapi'),
    path('api/process', views.ProcessListAPIView.as_view(), name='processapi'),
    path('api/network', views.ProcessListAPIView.as_view(), name='networkapi'),
]

defer(loop_logs)