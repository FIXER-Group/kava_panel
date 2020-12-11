from django.urls import path
from panel import views

app_name="panel"
urlpatterns = [
    path('', views.index, name='index'),
    path('process/', views.process, name='process'),
    path('logout/', views.logout_view, name='logout'),
    path('system/', views.system, name='system'),
    path('graphs/', views.graphs, name='graphs'),
    path('json/chart', views.LineChartJSONView.as_view(), name='chartJSON'),
    path('json/stats_update', views.stats_update, name='stats_update'),
]