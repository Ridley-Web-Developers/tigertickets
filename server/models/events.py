from datetime import timedelta, datetime

from pymongo.errors import DuplicateKeyError

from server.app import mongo

events = mongo.db.events

# converts date to day of week
d2d = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday'
}
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
columns = [[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
           [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
           [1, 2, 3, 4, 5, 6, 23, 24, 25, 26, 27, 28]]
# generates empty seat template
seats = [{'row': rows[i], 'column': j, 'scanned': False, 'person': {'_id': None, 'qr_string': ''}} for i in
         range(14) for j in columns[i]]


# generates a new year document template
def new_year_template(year, name, start_date, end_date, active=True, description=""):
    dates = [start_date + timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]
    return {
        '_id': year,  # _id is set to prevent duplicate years
        "year": year,
        "main_events": [
            {
                "name": name,
                "start_date": start_date,
                "end_date": end_date,
                "active": active,
                "description": description,
                "sessions": [{"session_date": i, "week": d2d[i.isoweekday()], "seats": seats} for i in dates]
            }
        ]
    }


# inserts new year document
def generate_new_year(year, name, start_date, end_date, active=True, description=""):
    """
    print(generate_new_year(2019, "The Farndale Dramatic Society's Production of Macbeth", datetime(2019, 10, 31),
                        datetime(2019, 11, 2), False, ''))
    """
    try:
        return events.insert_one(new_year_template(year, name, start_date, end_date, active, description))
    except DuplicateKeyError as error:
        return 'Duplicate Key Error: %s' % error


# add new event to specific year
def insert_new_event(year, name, start_date, end_date, active=True, description=""):
    """
    print(insert_new_event(2019, "Roald Dahl's Matilda the Musical", datetime(2020, 2, 27),
                       datetime(2020, 2, 29), False, ''))
    """
    events.update_many({}, {"$set": {"main_events.active": False}})
    dates = [start_date + timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]
    return events.update_one({"year": year}, {"$push": {
        "main_events": {
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "active": active,
            "description": description,
            "sessions": [{"session_date": i, "week": d2d[i.isoweekday()], "seats": seats} for i in dates]
        }}})


def update_seat_info(year, name, date, row, column, person_id, qr_string):
    return events.update_one(
        {"year": year, "main_events.name": name, "main_events.sessions.session_date": date,
         "main_events.sessions.seats.row": row, "main_events.sessions.seats.column": column},
        {"$set": {"main_events.$[].sessions.$[].seats.$[].scanned": False,
                  "main_events.$[].sessions.$[].seats.$[].person.person_id": person_id,
                  "main_events.$[].sessions.$[].seats.$[].person.qr_string": qr_string}})


def scan_seat(year, name, date, row, column):
    return events.update_one(
        {"year": year, "main_events.name": name, "main_events.sessions.session_date": date,
         "main_events.sessions.seats.row": row, "main_events.sessions.seats.column": column},
        {"$set": {"main_events.$[].sessions.$[].seats.$[].scanned": True}})


def find_user_seats(person_id, filter_options=None, options=None):
    person_filter = {"main_events.sessions.seats.person.id": person_id}
    filters = person_filter if filter_options is None else {**person_filter, **filter_options}
    if options is None:
        return [i for i in events.find(filters)]
    else:
        return [i for i in events.find(filters, options)]


def search_text(text, phrase=False, start_date=None, end_date=None):
    text = "\"%s\"" % text if phrase else text
    if start_date is None and end_date is None:
        return events.find({"$text": {"$search": text}},
                           {"main_events.name": 1, "main_events.description": 1, "score": {"$meta": "textScore"}}).sort(
            {"score": {"$meta": "textScore"}})
    # TODO: Finish implementation
    else:  # if start_date is not specified, search before, vice versa
        pass


# TODO: Finish implementation
def get_active_event(filters, projections):
    return events.find({"main_events.active": True})


def get_user_seating(user_id):
    return events.aggregate([
        {
            '$match': {
                'main_events.sessions.seats.person.id': user_id
            }
        }, {
            '$project': {
                'main_events.name': 1,
                'main_events.sessions.session_date': 1,
                'main_events.sessions.week': 1,
                'main_events.sessions.seats': 1
            }
        }, {
            '$unwind': {
                'path': '$main_events'
            }
        }, {
            '$unwind': {
                'path': '$main_events.sessions'
            }
        }, {
            '$match': {
                'main_events.sessions.seats.person.id': user_id
            }
        }, {
            '$unwind': {
                'path': '$main_events.sessions.seats'
            }
        }, {
            '$match': {
                'main_events.sessions.seats.person.id': user_id
            }
        }
    ])
