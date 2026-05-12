from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('experience/', views.experience, name='experience'),
    path('projects/', views.projects, name='projects'),
    path('skills/', views.skills, name='skills'),
    path('tools/', views.tools_list, name='tools'),
    path('tools/interval-timer/', views.interval_timer, name='interval_timer'),
    path('resume/', views.resume, name='resume'),
    path('contact/', views.contact_view, name='contact'),
]
