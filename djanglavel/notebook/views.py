from django.shortcuts import render

from .models import Contact

# Old style views

def index(request):
    result = {}
    result["contacts"] = Contact.objects.all()
    return render(request, 'notebook/index.html', result)
