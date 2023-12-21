from django.shortcuts import render

def index(request):
    return render(request, 'frontpage_app/index.html')

def product(request):
    return render(request, 'frontpage_app/product.html')