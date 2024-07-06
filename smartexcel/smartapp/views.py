from django.shortcuts import render

def default(request):
    return render(request, 'welcome.html')

def index(request):
    return render(request, 'form.html')
