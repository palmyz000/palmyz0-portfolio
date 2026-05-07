from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('experience/', views.experience, name='experience'),
    path('projects/', views.projects, name='projects'),
    path('skills/', views.skills, name='skills'),
    path('resume/', views.resume, name='resume'),
]
