from django.shortcuts import render

from .models import Contact


def index(request):
    """Old style view : just to show how it was done before
    """
    result = {}
    result["contacts"] = Contact.objects.all()
    return render(request, 'notebook/index.html', result)
