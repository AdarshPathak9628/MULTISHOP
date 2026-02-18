from django.shortcuts import render

# Temporary home view
def index(request):
    return render(request, 'store/index.html')