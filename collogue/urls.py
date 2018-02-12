from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings

from collogue.views import (HomeView, AddReservationView, GetReservationView, DeleteReservationView,
                            ApproveReservationView)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/', LoginView.as_view(template_name='collogue/login.html', extra_context={
        'app_name': settings.APP_NAME
    }), name='login'),
    url(r'^logout/', LogoutView.as_view(next_page='/'), name='logout'),

    url(r'^add-reservation/', AddReservationView.as_view(), name='add_reservation'),
    url(r'^get-reservation/(?P<range_from>\d{4}-\d{2}-\d{2})/(?P<to>\d{4}-\d{2}-\d{2})/(?P<room_pk>\d+)/',
        GetReservationView.as_view(), name='get_reservation'),
    url(r'^delete-reservation/(?P<res_pk>\d+)/', DeleteReservationView.as_view(), name='delete_reservation'),
    url(r'^approve-reservation/(?P<res_pk>\d+)/', ApproveReservationView.as_view(), name='approve_reservation')
]