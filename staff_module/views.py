from functools import wraps
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

MANAGE_STAFF_URL = "manage-staff/"


def __internal_role_classifier(user):
    """
    Redirects the user to the appropriate page based on their role.

    Args:
        user: The user object representing the logged-in user.

    Returns:
        A redirection to the appropriate page based on the user's role.
    """
    if user.is_superuser or user.is_administrator:
        return redirect(f"{MANAGE_STAFF_URL}admin/")
    elif user.is_manager:
        return redirect(f"{MANAGE_STAFF_URL}manager/")
    elif user.is_team_lead:
        return redirect(f"{MANAGE_STAFF_URL}team-leader/")
    else:  # TODO: redirect to employee page
        pass


def staff_role_required(view_func):
    """
    Decorator that checks if the user is authenticated and has the staff role.
    If the user is not authenticated, it redirects to the login page.
    """

    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")

        return __internal_role_classifier(request.user)

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
