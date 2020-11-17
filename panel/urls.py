from django.urls import path
from panel import views

app_name="panel"
urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout')
]