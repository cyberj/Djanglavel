from django.conf.urls import url

from . import views
from .views import index, ContactListView, ContactDetailView

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^list/', ContactListView.as_view(), name='list'),
    url(r'^detail/(?P<slug>[-\w\d]+)', ContactDetailView.as_view(), name='detail'),
]
