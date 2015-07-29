from django.conf.urls import url

from .views import index, ContactListView, ContactDetailView
from .views import ContactUpdateView, ContactCreateView, ContactDeleteView

urlpatterns = [
    url(r'^oldindex/$', index, name='index'),
    url(r'^contact/$', ContactListView.as_view(), name='list'),
    url(r'^contact/(?P<slug>[-\w\d]+)/$', ContactDetailView.as_view(), name='detail'),
    url(r'^contact/(?P<slug>[-\w\d]+)/update$', ContactUpdateView.as_view(), name='update'),
    url(r'^contact/(?P<slug>[-\w\d]+)/delete$', ContactDeleteView.as_view(), name='delete'),
    url(r'^contact/new$', ContactCreateView.as_view(), name='create'),
]
