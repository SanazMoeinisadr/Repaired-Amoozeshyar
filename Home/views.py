from django.shortcuts import render

def homePage(request):
    return render(request, 'Home/index.html', context={})

# Create your views here.
