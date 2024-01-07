from functools import wraps
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import resolve

MANAGE_STAFF_URL = "manage-staff/"


def __internal_role_classifier(user):
    """
    Determines the appropriate page URL based on the user's role.
    """
    if user.is_superuser or user.is_administrator:
        return f"/{MANAGE_STAFF_URL}admin/"
    elif user.is_manager:
        return f"/{MANAGE_STAFF_URL}manager/"
    elif user.is_team_lead:
        return f"/{MANAGE_STAFF_URL}team-leader/"
    else:
        return "/"  # TODO: redirect to employee page


def staff_role_required(view_func):
    """
    Decorator that checks if the user is authenticated and has the staff role.
    Redirects to the appropriate page if the user is trying to access an incorrect page for their role.
    """

    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        expected_url = __internal_role_classifier(request.user)
        current_url = request.path

        if expected_url and current_url not in expected_url:
            return HttpResponseRedirect(expected_url)

        return view_func(request, *args, **kwargs)

    return _wrapped_view


@staff_role_required
def manage_staff_classifier(request):
    return __internal_role_classifier(request.user)


@staff_role_required
def manage_staff_admin(request):
    return render(request, "staff_module/manage_staff_admin.html")


@staff_role_required
def manage_staff_manager(request):
    return render(request, "staff_module/manage_staff_manager.html")


@staff_role_required
def manage_staff_team_leader(request):
    return render(request, "staff_module/manage_staff_team_leader.html")
