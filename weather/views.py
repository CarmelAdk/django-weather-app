from django.shortcuts import render

def index(request):
    context = {
        'city'
    }
    return render(request, 'weather/index.html')
