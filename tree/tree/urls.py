from django.contrib import admin
from django.urls import path

import menu_app.views as views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("about/history", views.history, name="history"),
    path("about/team/", views.team, name="team"),
    path("about/team/backend/", views.team_backend, name="team_backend"),
    path("about/team/backend/back1", views.back1, name="back1"),
    path("about/team/backend/back2/", views.back2, name="back2"),
    path("about/team/frontend/", views.team_frontend, name="team_frontend"),
    path("about/team/frontend/front1/", views.front1, name="front1"),
    path("about/team/frontend/front2/", views.front2, name="front2"),
    path("contacts/", views.contacts, name="contacts"),
    path("services/", views.services, name="services"),
    path("services/audit/", views.audit, name="audit"),
]
