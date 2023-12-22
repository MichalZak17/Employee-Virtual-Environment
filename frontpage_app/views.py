from django.shortcuts import render

def index(request):
    return render(request, 'frontpage_app/index.html')

def product(request):
    return render(request, 'frontpage_app/product.html')

def use_cases(request):
    return render(request, 'frontpage_app/use_cases.html')

def contact_us(request):
    return render(request, 'frontpage_app/contact_us.html')