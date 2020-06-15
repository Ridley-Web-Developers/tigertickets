from django.conf.urls import url, include, re_path
from django.urls import path
from django.views.generic import ListView, DetailView

from . import views
from .models import *

app_name = 'tickets'
urlpatterns = [
    path('home', views.home_page, name='home'),
    path('purchase', views.purchase),
    path('history-awards', views.mandeville),
    path('team', views.about_us),
    path('events', views.all_events),
    path('events',
         ListView.as_view(queryset=Event.objects.all().order_by("-date"),
                          template_name='tickets/event_list.html')),
    re_path(r'^events/(?P<pk>\d+)/$', DetailView.as_view(model=Event,
                                                         template_name='tickets/event.html')),
    re_path('signup', views.user_signup, name='register_user'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate_account, name='activate'),
    path('seat_selection/<str:session>', views.seat_selection),
    path('email/<str:session>/<str:seats>', views.email),
    path('success', views.success),
    path('modify', views.modify),
    path('seat_list/<str:email>', views.seat_list),
]
