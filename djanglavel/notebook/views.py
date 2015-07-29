from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Contact


def index(request):
    """Old style view : just to show how it was done before
    """
    result = {}
    result["contacts"] = Contact.objects.all()
    return render(request, 'notebook/index.html', result)


class ContactListView(ListView):

    model = Contact
    context_object_name = "contacts"


class ContactListDetail(DetailView):

    model = Contact
    context_object_name = "contact"
