from datetime import datetime as dt
from datetime import timedelta

import pandas as pd

# print _compare_distance(52.2296756, 21.0122287, 52.406374, 16.9251681)
from nomad.models import Journey, Category, User


def _compare_distance(lat_one, long_one, lat_two, long_two):
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat_one)
    lon1 = radians(long_one)
    lat2 = radians(lat_two)
    lon2 = radians(long_two)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return int(distance)


# datetime_object = dt.strptime('20170630', "%Y%m%d")
# print _compare_dates('20170625', '20170630', '20170625', '20170630')
def _compare_dates(from_date_one, to_date_one, from_date_two, to_date_two):
    start_date_one = __get_date(from_date_one)
    finish_date_one = __get_date(to_date_one)

    start_date_two = __get_date(from_date_two)
    finish_date_two = __get_date(to_date_two)

    from collections import namedtuple
    Range = namedtuple('Range', ['start', 'end'])
    r1 = Range(start_date_one, finish_date_one)
    r2 = Range(start_date_two, finish_date_two)

    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)

    overlap = (earliest_end - latest_start).days + 1

    overlapped_days = []
    for i in range(overlap):
        overlapped_day = earliest_end - timedelta(i)
        overlapped_days.append(overlapped_day)

    return overlapped_days


def __get_pd_jorneys():
    keys = ['username', 'fromDate', 'toDate', 'username_id', 'longitude', 'latitude']
    return pd.DataFrame([[getattr(i, j) for j in keys] for i in Journey.objects.all()], columns=keys)


def __get_pd_categories():
    keys = ['username_id', 'category_id']
    return pd.DataFrame([[getattr(i, j) for j in keys] for i in Category.objects.all()], columns=keys)


def __get_pd_users():
    keys = ['username']
    return pd.DataFrame([[getattr(i, j) for j in keys] for i in User.objects.all()], columns=keys)


def __get_date(date_str):
    return dt.strptime(date_str, "%Y%m%d")


def calculate_scores(search_user):
    journeys = __get_pd_jorneys()
    users = __get_pd_users()
    cats = __get_pd_categories()

    scores = []

    for index, other in users[users['username'] != search_user].iterrows():
        match_user = other['username']

        matched_journeys = pd.DataFrame(columns=journeys.keys())
        overlapped_days_unique = set()

        this_j_all = journeys[journeys['username_id'] == search_user]
        for index_two, this_j in this_j_all.iterrows():
            other_j_all = journeys[journeys['username_id'] == match_user]

            for index_three, other_j in other_j_all.iterrows():
                distance = _compare_distance(float(this_j['latitude']), float(this_j['longitude']),
                                             float(other_j['latitude']), float(other_j['longitude']))

                other_j['fromDate_search'] = this_j['fromDate']
                other_j['toDate_search'] = this_j['toDate']

                if distance < 50:
                    matched_journeys = matched_journeys.append(other_j)

            overlapped_days = []
            for index_three, matched_j in matched_journeys.iterrows():
                delta_days = _compare_dates(str(matched_j['fromDate_search']), str(matched_j['toDate_search']),
                                            str(matched_j['fromDate']), str(matched_j['toDate']))
                overlapped_days.append(delta_days)

            for days in overlapped_days:
                for day in days:
                    overlapped_days_unique.add(day)

        search_cats = cats[cats['username_id'] == search_user]['category_id']
        m_cats = cats[cats['username_id'] == match_user]['category_id']

        match_cat_count = 0
        for cat in search_cats:
            if m_cats[m_cats == cat].any():
                match_cat_count += 1

        scores.append([match_user, len(overlapped_days_unique) * match_cat_count])

    return scores

# if __name__ == "__main__":
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#
#     from django.core.management import execute_from_command_line
#
#     execute_from_command_line(sys.argv)
#
#     from nomad.models import User, Journey, Category
#
#     calculate_scores('adasd')
#
#     print ''
# print _compare_dates('20170625', '20170630', '20170625', '20170630')
