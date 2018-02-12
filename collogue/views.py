import json
from datetime import datetime

from django.shortcuts import render
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.core.mail import send_mail
from django.urls import reverse

from collogue import urljoin
from collogue.models import Room, Reservation


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        urls = {
            'add_reservation': urljoin('/', settings.URL_PREFIX, 'add-reservation'),
            'get_reservation': urljoin('/', settings.URL_PREFIX, 'get-reservation'),
            'delete_reservation': urljoin('/', settings.URL_PREFIX, 'delete-reservation'),
        }
        context = {
            'rooms': Room.objects.all(),
            'app_name': settings.APP_NAME,
            'urls': urls
        }

        return render(request, 'collogue/home.html', context)


class AddReservationView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            res_start = datetime.strptime(request.GET['start_time'], '%Y-%m-%dT%H:%M:%S')
            res_end = datetime.strptime(request.GET['end_time'], '%Y-%m-%dT%H:%M:%S')

            res = Reservation(
                room=Room.objects.get(pk=int(request.GET['room'])),
                name=request.GET['name'],
                description=request.GET['description'],
                reserved_by=request.user,
                start_time=res_start,
                end_time=res_end,
                recurrence_rule_args=None
            )
            res.save()

            # Send out email
            if settings.SEND_APPROVER_EMAIL:
                approve_url = urljoin(
                    settings.URL_HOSTNAME,
                    settings.URL_PREFIX,
                    reverse('approve_reservation', args=(res.pk,))
                )
                msg = ('Room: {room}{{nl}}'
                       'Name: {name}{{nl}}'
                       'For: {start} to {end}{{nl}}'
                       'Description: {description}{{nl}}'
                       '{{nl}}'  #TODO Add Recurrence
                       '{{approval}}').format(
                    room=res.room.name,
                    name=res.name,
                    start=res.start_time.strftime('%I:%M%p'),
                    end=res.end_time.strftime('%I:%M%p'),
                    description=res.description
                )
                send_mail(
                    subject='Reservation {} Pending Approval'.format(res.name),
                    message=msg.format(
                        nl='\n',
                        approval='Please visit the admin site or point your browser to {}'.format(approve_url)
                    ),
                    html_message=msg.format(
                        nl='<br/>',
                        approval='<a href="{}">Approve this reservation</a>'.format(approve_url)
                    ),
                    from_email='reservation@igsb.uchicago.edu',
                    recipient_list=settings.APPROVER_EMAILS
                )

            return HttpResponse(json.dumps({'result': 'success', 'id': res.pk}))
        except Exception as e:
            return HttpResponse(json.dumps({'result': 'error', 'error': str(e)}))


class GetReservationView(View):
    def get(self, request, range_from, to, room_pk):
        # TODO This eventually needs to account for recurrences
        return HttpResponse(json.dumps(
            Reservation.get_reservations(
                range_from=datetime.strptime(range_from, '%Y-%m-%d').date(),
                to=datetime.strptime(to, '%Y-%m-%d').date(),
                room_pk=room_pk
            )
        ))


class DeleteReservationView(LoginRequiredMixin, View):
    def get(self, request, res_pk):
        try:
            Reservation.objects.get(pk=res_pk).delete()
            return HttpResponse(json.dumps({'result': 'success'}))
        except Exception as e:
            return HttpResponse(json.dumps({'result': 'error', 'error': str(e)}))


class ApproveReservationView(LoginRequiredMixin, View):
    def get(self, request, res_pk):
        if request.user.is_staff:
            res = Reservation.objects.get(pk=res_pk)
            res.approved = True
            res.save()
            return HttpResponse('Success')
        return HttpResponse('You are not authorized to approve reservations')