from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("admin/dashboard/")
        return view_func(request, *args, **kwargs)

    return wrapper


@redirect_authenticated_user
def index(request):
    return render(request, "frontend/home.html")


@redirect_authenticated_user
def product(request):
    return render(request, "frontend/product.html")


@redirect_authenticated_user
def use_cases(request):
    return render(request, "frontend/use_cases.html")


@redirect_authenticated_user
def contact_us(request):
    return render(request, "frontend/contact_us.html")


def team_leader_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        elif not request.user.user_is_team_lead:
            return redirect("/login/")
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required(login_url="/login/")
@team_leader_required
def dashboard(request):
    return render(request, "frontend/dashboard.html")
