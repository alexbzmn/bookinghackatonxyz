from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


@python_2_unicode_compatible
class EventsRequest(object):
    def __init__(self, longitude=None, latitude=None, categories=None, fromDate=None, toDate=None):
        self.longitude = longitude
        self.latitude = latitude
        self.categories = categories
        self.fromDate = fromDate
        self.toDate = toDate

    def __str__(self):
        return self.longitude + ' ' + self.latitude


@python_2_unicode_compatible
class EventsResponse(object):
    def __init__(self, events=None):
        self.events = events

    def __str__(self):
        return self.events


@python_2_unicode_compatible
class Event(object):
    def __init__(self, eventId=None, title=None, tags=None, startDateTime=None, description=None, longitude=None,
                 latitude=None, imageUrl=None, eventUrl=None, service_id=None):
        self.eventId = eventId
        self.title = title
        self.tags = tags
        self.startDateTime = startDateTime
        self.description = description
        self.longitude = longitude
        self.latitude = latitude
        self.imageUrl = imageUrl
        self.eventUrl = eventUrl
        self.service_id = service_id

    @staticmethod
    def from_json(event, event_request=None):
        current_event = Event()
        current_event.title = event['title']
        current_event.description = event['description']

        image = event['image']
        if image is not None:
            current_event.imageUrl = get_image(image)

        current_event.latitude = event['latitude']
        current_event.longitude = event['longitude']
        current_event.startDateTime = event['start_time']
        current_event.eventId = event['id']
        current_event.service_id = 'eventful'
        current_event.eventUrl = event['url']

        if event_request is not None:
            current_event.tags = event_request.categories

        return current_event

    @staticmethod
    def get_image(image):
        if 'medium' in image:
            return image['medium']['url']
        return ""

    def __str__(self):
        return self.eventId
