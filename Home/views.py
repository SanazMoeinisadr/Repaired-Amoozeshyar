from django.shortcuts import render

def homePage(request):
    return render(request, 'Home/index.html', context={})

def contactUS(request):
    return render(request, 'Home/contactUs.html', context={})

# Create your views here.
