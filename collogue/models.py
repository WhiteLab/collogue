from datetime import datetime
import pickle
import uuid

from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField('Room Name', max_length=256)
    description = models.TextField('Room Description', blank=True, null=True)

    def __unicode__(self):
        return 'Room {}'.format(self.name)

    def __str__(self):
        return self.__unicode__()


class Reservation(models.Model):
    room = models.ForeignKey('Room')
    name = models.CharField('Reservation Event Name', max_length=1024)
    description = models.TextField('Reservation Event Description', blank=True, null=True)
    reserved_by = models.ForeignKey(User)
    start_time = models.DateTimeField('Reservation Start Time')
    end_time = models.DateTimeField('Reservation End Time')
    recurrence_rule_args = models.BinaryField('Reservation Recurrence Rule', blank=True, null=True,
                                              help_text='JSON representation of the arguments to a '
                                                        'dateutil.rrule.rrule for this Reservation')
    approved = models.BooleanField('Approved', default=False)
    equipment_request = None
    participants = None

    class Meta:
        ordering = ['-start_time']

    @staticmethod
    def get_reservations(range_from, to, room_pk=None):
        """
        Given a date range returns all reservations that occur within the range,
        accounting for recurrences.

        :param range_from:
        :param to:
        :return:
        """
        reservations = list()
        all_res = Reservation.objects.filter(room__pk=room_pk)
        for res in all_res:
            # Check if a recurrence falls into this range
            if res.recurrence_rule_args:
                rrule_res = [
                    r for r in list(pickle.loads(res.recurrence_rule_args))
                    if range_from <= r.date() <= to
                ]
                for rrule_res_ in rrule_res:
                    reservations.append({
                        'start': rrule_res_.strftime('%Y-%m-%dT%H:%M:%S'),
                        'end': (rrule_res_ + (res.end_time - res.start_time)).strftime('%Y-%m-%dT%H:%M:%S'),
                        'id': str(res.pk) + str(uuid.uuid4())[:8],
                        'text': '<b>{name}{unapproved}</b><br/>{start} - {end}<br/>{description}'.format(
                            name=res.name,
                            unapproved=' (Unapproved)' if not res.approved else '',
                            start=res.start_time.strftime('%I:%M%p'),
                            end=res.end_time.strftime('%I:%M%p'),
                            description=res.description
                        ),
                        'backColor': '#CED3DC' if res.approved else '#F4DFB7',
                        'borderColor': 'transparent'
                    })
            elif res.start_time.date() >= range_from and res.end_time.date() <= to:
                reservations.append({
                    'start': res.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'end': res.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'id': res.pk,
                    'text': '<b>{name}{unapproved}</b><br/>{start} - {end}<br/>{description}'.format(
                        name=res.name,
                        unapproved=' (Unapproved)' if not res.approved else '',
                        start=res.start_time.strftime('%I:%M%p'),
                        end=res.end_time.strftime('%I:%M%p'),
                        description=res.description
                    ),
                    'backColor': '#CED3DC' if res.approved else '#F4DFB7',
                    'borderColor': 'transparent'
                })
        return reservations

    def date(self):
        return self.start_time.date()

    def __unicode__(self):
        return 'Reservation: {name} {at}'.format(
            name=self.name,
            at=self.start_time
        )

    def __str__(self):
        return self.__unicode__()
