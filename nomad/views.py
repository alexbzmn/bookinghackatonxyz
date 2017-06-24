from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import json

from nomad.api.event_api import EventfulDataImporter
from nomad.app_constants import EVENT_CATEGORIES
from nomad.models import LikedEvent
from .models import Question, Choice, EventRequest, Event, LikeRequest


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'nomad/index.html', context)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def create_question_view(request, arg):
    return render(request, 'nomad/createq.html')


def create_question_create(request, arg):
    questionJSON = json.loads(request.body)

    question = Question()
    question.question_text = str(questionJSON.get("Text"))
    question.pub_date = timezone.now()

    question.save()

    return HttpResponse("Question is created")


def create_question_create(request, arg):
    questionJSON = json.loads(request.body)

    question = Question()
    question.question_text = str(questionJSON.get("Text"))
    question.pub_date = timezone.now()

    question.save()

    return HttpResponse("Question is created")


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'nomad/detail.html', {'question': question})


def get_events(request, arg):
    if (request.method == 'POST'):
        eventsRequestJSON = json.loads(request.body)
        eventRequest = EventRequest()
        eventRequest.latitude = str(eventsRequestJSON.get("latitude"))
        eventRequest.longitude = str(eventsRequestJSON.get("longitude"))
        eventRequest.fromDate = str(eventsRequestJSON.get("fromDate"))
        eventRequest.toDate = str(eventsRequestJSON.get("toDate"))
        eventRequest.categories = eventsRequestJSON.get("categories")
        eventRequest.username = eventsRequestJSON.get("username")
        categoryNames = []

        for category in eventRequest.categories:
            categoryNames.append(EVENT_CATEGORIES[category])

        categories = ",".join(categoryNames)

        importer = EventfulDataImporter()
        if eventRequest.fromDate is not None and eventRequest.toDate is not None:
            date_interval = '{0}00-{1}00'.format(eventRequest.fromDate, eventRequest.toDate)
            events = importer.import_events(lat=float(eventRequest.latitude), long=float(eventRequest.longitude),
                                            categories=categories, date_interval=date_interval)
        else:
            events = importer.import_events(lat=float(eventRequest.latitude), long=float(eventRequest.longitude),
                                            categories=categories)

        events_array = []
        for event in events:
            current_event = Event.from_json(event, eventRequest)
            events_array.append(current_event)

        json_resp = json.dumps(events_array, default=lambda o: o.__dict__)
        return HttpResponse(json_resp)
    return HttpResponse("Get Event request is not supported")


def likeDeprecated(request, service_id, event_id):
    if request.method == 'POST':
        importer = EventfulDataImporter()
        return HttpResponse('serviceId {0} , id {1}'.format(service_id, event_id))
    return HttpResponse("Get Event request is not supported")


def like(request, args):
    if request.method == 'POST':
        likeRequestJSON = json.loads(request.body)
        likeRequest = LikeRequest()
        likeRequest.username = likeRequestJSON.get("username")
        likeRequest.event_id = likeRequestJSON.get("event_id")
        likeRequest.service_id = likeRequestJSON.get("service_id")

        importer = EventfulDataImporter()

        event = importer.get_event_by_id(event_id=likeRequest.event_id)

        liked_event = LikedEvent()
        liked_event.id = likeRequest.event_id + likeRequest.username
        liked_event.event_id = likeRequest.event_id
        liked_event.username = likeRequest.username
        liked_event.service_id = likeRequest.service_id
        liked_event.latitude = event.latitude
        liked_event.longitude = event.longitude
        liked_event.title = event.title
        liked_event.description = event.description
        liked_event.start_time = event.startDateTime
        liked_event.event_url = event.eventUrl
        liked_event.image_url = event.imageUrl

        liked_event.save()

        return HttpResponse('Post like successful')
    return HttpResponse("Get Event request is not supported")
