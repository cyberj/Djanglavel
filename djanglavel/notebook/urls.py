from django.conf.urls import url

from . import views
from .views import index, ContactListView

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^list/', ContactListView.as_view(), name='list')
    # url(r'^$(?P<slug>[-\w\d]+)/$', views.detail, name='detail'),
]
