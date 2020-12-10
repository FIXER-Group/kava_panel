from django.urls import path
from panel import views
from .views import  line_chart_json

app_name="panel"
urlpatterns = [
    path('', views.index, name='index'),
    path('process/', views.process, name='process'),
    path('logout/', views.logout_view, name='logout'),
    path('system/', views.system, name='system'),
    path('graphs/', views.graphs, name='graphs'),
    path('chartJSON/', line_chart_json, name='chartJSON'),
    path('json/stats_update', views.stats_update, name='stats_update'),
]