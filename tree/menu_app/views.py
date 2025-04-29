from django.shortcuts import render


def home(request):
    return render(request, "base.html")


def about(request):
    return render(request, "pages/about.html")


def history(request):
    return render(request, "pages/history.html")


def team(request):
    return render(request, "pages/team.html")


def team_backend(request):
    return render(request, "pages/team_backend.html")


def back1(request):
    return render(request, "pages/back1.html")


def back2(request):
    return render(request, "pages/back2.html")


def team_frontend(request):
    return render(request, "pages/team_frontend.html")


def front1(request):
    return render(request, "pages/front1.html")


def front2(request):
    return render(request, "pages/front2.html")


def contacts(request):
    return render(request, "pages/contacts.html")


def services(request):
    return render(request, "pages/services.html")


def audit(request):
    return render(request, "pages/audit.html")
