from django.shortcuts import render, redirect

def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@redirect_authenticated_user
def index(request):
    return render(request, 'frontpage_app/index.html')

@redirect_authenticated_user
def product(request):
    return render(request, 'frontpage_app/product.html')

@redirect_authenticated_user
def use_cases(request):
    return render(request, 'frontpage_app/use_cases.html')

@redirect_authenticated_user
def contact_us(request):
    return render(request, 'frontpage_app/contact_us.html')

# Create your views here.
def dashboard(request):
    return render(request, 'frontend/dashboard.html')