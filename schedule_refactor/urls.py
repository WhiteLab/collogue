from django.conf.urls import url
from django.views.generic.list import ListView
# from django.views.generic.list_detail import object_list
from schedule_refactor.models import Room
from schedule_refactor.feeds import UpcomingReservationsFeed
from schedule_refactor.feeds import RoomIRoom
from schedule_refactor.periods import Year, Month, Week, Day
import schedule_refactor.views

info_dict = {
    'queryset': Room.objects.all(),
}

urlpatterns = ['',

# urls for Rooms
url(r'^room/$',
    ListView.as_view(queryset=Room.objects.all(), template_name='schedule/room_list.html'),
    name="schedule"),

url(r'^room/year/(?P<room_slug>[-\w]+)/$',
    'schedule_refactor.views.room_by_periods',
    name="year_room",
    kwargs={'periods': [Year], 'template_name': 'schedule/room_year.html'}),

url(r'^room/tri_month/(?P<room_slug>[-\w]+)/$',
    'schedule_refactor.views.room_by_periods',
    name="tri_month_room",
    kwargs={'periods': [Month], 'template_name': 'schedule/room_tri_month.html'}),

url(r'^room/compact_month/(?P<room_slug>[-\w]+)/$',
    'schedule_refactor.views.room_by_periods',
    name = "compact_room",
    kwargs={'periods': [Month], 'template_name': 'schedule/room_compact_month.html'}),

url(r'^room/month/(?P<room_slug>[-\w]+)/$',
    'schedule_refactor.views.room_by_periods',
    name = "month_room",
    kwargs={'periods': [Month], 'template_name': 'schedule/room_month.html'}),

url(r'^room/week/(?P<room_slug>[-\w]+)/$',
    'schedule_refactor.views.room_by_periods',
    name = "week_room",
    kwargs={'periods': [Week], 'template_name': 'schedule/room_week.html'}),

url(r'^room/daily/(?P<room_slug>[-\w]+)/$',
    'schedule_refactor.views.room_by_periods',
    name = "day_room",
    kwargs={'periods': [Day], 'template_name': 'schedule/room_day.html'}),

url(r'^room/(?P<room_slug>[-\w]+)/$',
    'schedule_refactor.views.room',
    name = "room_home",
    ),

#Reservation Urls
url(r'^reservation/create/(?P<room_slug>[-\w]+)/$',
    'schedule_refactor.views.create_or_edit_reservation',
    name='room_create_reservation'),
url(r'^reservation/edit/(?P<room_slug>[-\w]+)/(?P<reservation_id>\d+)/$',
    'schedule_refactor.views.create_or_edit_reservation',
    name='edit_reservation'),
url(r'^reservation/(?P<reservation_id>\d+)/$',
    'schedule_refactor.views.reservation',
    name="reservation"), 
url(r'^reservation/delete/(?P<reservation_id>\d+)/$',
    'schedule_refactor.views.delete_reservation',
    name="delete_reservation"),

#urls for already persisted occurrences
url(r'^occurrence/(?P<reservation_id>\d+)/(?P<occurrence_id>\d+)/$',
    'schedule_refactor.views.occurrence',
    name="occurrence"), 
url(r'^occurrence/cancel/(?P<reservation_id>\d+)/(?P<occurrence_id>\d+)/$',
    'schedule_refactor.views.cancel_occurrence',
    name="cancel_occurrence"),
url(r'^occurrence/edit/(?P<reservation_id>\d+)/(?P<occurrence_id>\d+)/$',
    'schedule_refactor.views.edit_occurrence',
    name="edit_occurrence"),

#urls for unpersisted occurrences
url(r'^occurrence/(?P<reservation_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/(?P<second>\d+)/$',
    'schedule_refactor.views.occurrence',
    name="occurrence_by_date"),
url(r'^occurrence/cancel/(?P<reservation_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/(?P<second>\d+)/$',
    'schedule_refactor.views.cancel_occurrence',
    name="cancel_occurrence_by_date"),
url(r'^occurrence/edit/(?P<reservation_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/(?P<second>\d+)/$',
    'schedule_refactor.views.edit_occurrence',
    name="edit_occurrence_by_date"),
    

#feed urls 
url(r'^feed/room/(.*)/$',
    'django.contrib.syndication.views.feed', 
    { "feed_dict": { "upcoming": UpcomingReservationsFeed } }),
 
(r'^ical/room/(.*)/$', RoomIRoom()),

 url(r'^$', ListView.as_view(queryset=Room.objects.all()), name='schedule'),
]
