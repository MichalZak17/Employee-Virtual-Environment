from django.shortcuts import render

# Create your views here.
def manage_staff(request):
    return render(request, 'staff_module/manage_staff.html')