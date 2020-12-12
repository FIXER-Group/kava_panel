from django.urls import path
from panel import views
from .models import loop_logs
from django_simple_task import defer


app_name="panel"
urlpatterns = [
    path('', views.index, name='index'),
    path('process/', views.process, name='process'),
    path('network/', views.network, name='network'),
    path('logout/', views.logout_view, name='logout'),
    path('system/', views.system, name='system'),
    path('json/chartcpu', views.LineChartCpu.as_view(), name='chartcpu'),
    path('json/chartram', views.LineChartRam.as_view(), name='chartram'),
    path('json/stats_update', views.stats_update, name='stats_update'),
]

defer(loop_logs)