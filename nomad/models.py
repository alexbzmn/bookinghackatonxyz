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
class User(models.Model):
    username = models.CharField(primary_key=True, max_length=200)

    def __str__(self):
        return self.username


@python_2_unicode_compatible
class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    category_id = models.IntegerField()
    username = models.ForeignKey(User)

    def __str__(self):
        return "id = {0}, username = {1}".format(self.id, self.username)


@python_2_unicode_compatible
class EventRequest(object):
    def __init__(self, longitude=None, latitude=None, categories=None, fromDate=None, toDate=None, username=None):
        self.username = username
        self.longitude = longitude
        self.latitude = latitude
        self.categories = categories
        self.fromDate = fromDate
        self.toDate = toDate

    def __str__(self):
        return self.longitude + ' ' + self.latitude


@python_2_unicode_compatible
class Journey(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.ForeignKey(User)
    fromDate = models.CharField(max_length=100)
    toDate = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)

    def __str__(self):
        return "id = {0}, username = {1}".format(self.id, self.username)


@python_2_unicode_compatible
class LikedEvent(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    event_id = models.CharField(max_length=100)
    service_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)
    start_time = models.CharField(max_length=100, null=True)
    event_url = models.CharField(max_length=1000, null=True)
    image_url = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return "id = {0}, username = {1}".format(self.event_id, self.username)


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

        current_event.imageUrl = Event.get_image(event)

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
    def get_image(event):
        image_tag = 'image'

        if image_tag not in event:
            return ''

        image = event[image_tag]
        if image is None:
            return ''

        if 'medium' in image:
            return image['medium']['url']
        return ''

    def __str__(self):
        return self.eventId


@python_2_unicode_compatible
class LikeRequest(object):
    def __init__(self, service_id=None, event_id=None, username=None):
        self.service_id = service_id
        self.event_id = event_id
        self.username = username

    def __str__(self):
        return 'service_id {0} , event_id {1}, username {2}'.format(self.service_id, self.event_id, self.username)
