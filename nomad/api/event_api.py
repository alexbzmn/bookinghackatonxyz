import eventful

from nomad.models import Event


class EventfulDataImporter:
    """
    Event data importer.
    Invokes eventful rest API and retrieves event data using specified criterion.
    You can specify 'date' parameter to fetch some specific date interval or use the default one:

    """

    def __init__(self, api_key='cZswvGgQpFhXMDVZ'):
        self.api_key = api_key

    def import_events(self, lat, long, categories, date_interval='2009042500-2017042700'):
        eventful_api = eventful.API(self.api_key)
        data_list = []

        location_str = '{0},{1}'.format(lat, long)

        try:
            within_param = 10
            page_size_param = 100
            page_count = 1
            request_resource = '/events/search'

            res = eventful_api.call(request_resource, page_count=page_count, category=categories, location=location_str,
                                    within=within_param,
                                    page_size=page_size_param,
                                    date=date_interval)
            data_list.append(res)

        except:
            print 'Eventful request error'

        return data_list[0]['events']['event']

    def get_event_by_id(self, event_id):
        eventful_api = eventful.API(self.api_key)
        event = None

        try:
            request_resource = '/events/get'

            event = eventful_api.call(request_resource, id=event_id)

        except:
            print 'Eventful request error for event: '.format(event_id)

        return Event.from_json(event)

# Example
# importer = EventfulDataImporter()
# events = importer.get_event_by_id(event_id="E0-001-095008330-1")

# print events
