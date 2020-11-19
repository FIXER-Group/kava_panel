from django.urls import path
from panel import views

app_name="panel"
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    path('json/stats_update', views.stats_update, name='stats_update')
]