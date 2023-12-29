from . import models
from functools import wraps
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required


def check_permission(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and (
            user.is_superuser
            or user.is_staff
            or user.user_is_administrator
            or user.user_is_manager
        ):
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "Permission denied"}, status=403)

    return wrapper


@login_required
@check_permission
def manage_staff(request):
    return render(request, "staff_module/manage_staff.html")


@login_required
@check_permission
def get_all_languages(request):
    languages = models.CustomUser.USER_LANGUAGE_CHOICES
    return JsonResponse({"languages": languages})


@login_required
@check_permission
def get_all_contracts(request):
    contracts = models.CustomUser.USER_CONTRACT_CHOICES
    return JsonResponse({"contracts": contracts})


@login_required
@check_permission
def get_all_sites(request):
    sites = models.CustomUser.USER_SITE_CHOICES
    return JsonResponse({"sites": sites})


@login_required
@check_permission
def create_user(request):
    if not request.method == "POST":
        return HttpRequest("Method not allowed", status=405)

    user = request.user

    if not user.user_team:
        return HttpRequest("You don't have team", status=403)
