from datetime import timedelta, datetime

from pymongo.errors import DuplicateKeyError

from server.app import mongo

events = mongo.db.events
seats = mongo.db.seats
users = mongo.db.users

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


def generate_seats(year, name, date):
    # generates empty seat template
    seats_template = [
        {'year': year, 'name': name, 'date': date, 'row': rows[i], 'column': j, 'scanned': False, 'person_id': None,
         'qr_string': ''} for i in
        range(14) for j in columns[i]]
    result = seats.insert_many(seats_template)
    ids = result.inserted_ids
    return events.update_one({'year': year, 'main_events.name': name, 'main_events.sessions.session_date': date},
                             {'$set': {'main_events.$[].sessions.$[].seats': ids}})


# generates a new year document template
def new_year_template(year, name, start_date, end_date, active=True, description=""):
    events.update_many({}, {"$set": {"main_events.$[].active": False}})
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
                "sessions": [{"session_date": i, "week": d2d[i.isoweekday()], "seats": []} for i in dates]
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
        dates = [start_date + timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]
        result = events.insert_one(new_year_template(year, name, start_date, end_date, active, description))
        for date in dates:
            generate_seats(year, name, date)
        return result
    except DuplicateKeyError as error:
        return 'Duplicate Key Error: %s' % error


# add new event to specific year, check for duplicates
def insert_new_event(year, name, start_date, end_date, active=True, description=""):
    """
    print(insert_new_event(2019, "Roald Dahl's Matilda the Musical", datetime(2020, 2, 27),
                       datetime(2020, 2, 29), False, ''))
    """
    events.update_many({}, {"$set": {"main_events.$[].active": False}})
    dates = [start_date + timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]
    result = events.update_one({"year": year}, {"$push": {
        "main_events": {
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "active": active,
            "description": description,
            "sessions": [{"session_date": i, "week": d2d[i.isoweekday()], "seats": []} for i in dates]
        }}})
    for date in dates:
        generate_seats(year, name, date)
    return result


def generate_user(first_name, last_name, username, password, email):
    user_info = {'first_name': first_name, 'last_name': last_name, 'username': username, 'password': password,
                 'email': email, 'connections': None, 'seats': [], 'history': []}
    return users.insert_one(user_info)


# TODO: Make sure that there are no duplicate emails (or not)
def get_user_by_email(email):
    return users.find({'email': email})


# TODO: Make sure that there are no duplicate usernames
def get_user_by_username(username):
    return users.find_one({'username': username})


def user_add_seat(person_id, seat_id):
    return users.update_one({'_id': person_id}, {'$push': {'seats': seat_id}})


def user_delete_seat(person_id, seat_id):
    return users.update_one({'_id': person_id}, {'$pull': {'seats': {'$eq': seat_id}}})


# TODO: Remove project seats._id
def fetch_seat(year, name, date, row, column, _id=True):
    result = list(events.aggregate(
        [{'$match': {'year': year, 'main_events.name': name,
                     'main_events.sessions.session_date': date}},
         {'$lookup': {'from': 'seats', 'localField': 'main_events.sessions.seats', 'foreignField': '_id',
                      'as': 'seats'}},
         {'$project': {"seats": 1, '_id': 0}}, {
             '$unwind': {
                 'path': '$seats'
             }
         }, {'$match': {'seats.row': row, 'seats.column': column}}, {'$project': {"seats._id": 1}}]))[0]['seats']
    return result['_id'] if _id else result


# TODO: update user seat
def update_seat_add(year, name, date, row, column, person_id, qr_string):
    seat_info = fetch_seat(year, name, date, row, column, _id=False)
    user_add_seat(person_id, seat_info)
    return seats.update_one(
        {"_id": seat_info['_id']},
        {"$set": {"scanned": False, "person_id": person_id, "qr_string": qr_string}})


def update_seat_delete(year, name, date, row, column, person_id, qr_string):
    seat_info = fetch_seat(year, name, date, row, column, _id=False)
    user_delete_seat(person_id, seat_info)
    return seats.update_one(
        {"_id": seat_info['_id']},
        {"$set": {"scanned": False, "person_id": person_id, "qr_string": qr_string}})


def scan_seat(year, name, date, row, column):
    seat_id = fetch_seat(year, name, date, row, column)
    return seats.update_one(
        {"_id": seat_id},
        {"$set": {"scanned": True}})


def find_user_seats(person_id, filter_options=None, options=None):
    result = list(users.aggregate(
        [{'$match': {'_id': person_id}},
         {'$lookup': {'from': 'seats', 'localField': 'seats', 'foreignField': '_id',
                      'as': 'seats'}},
         {'$project': {"seats": 1, '_id': 0}}, {
             '$unwind': {
                 'path': '$seats'
             }
         }, {'$project': {"seats._id": 1}}]))[0]['seats']
    return result


def search_text(text, phrase=False, start_date=None, end_date=None):
    text = "\"%s\"" % text if phrase else text
    if start_date is None and end_date is None:
        return events.find({"$text": {"$search": text}},
                           {"main_events.name": 1, "main_events.description": 1, "score": {"$meta": "textScore"}}).sort(
            {"score": {"$meta": "textScore"}})
    # TODO: Finish implementation
    else:  # if start_date is not specified, search before, vice versa
        date_filter = []
        if start_date is not None:
            date_filter.append({
                'main_events.end_date': {
                    '$lt': end_date
                }})
        if end_date is not None:
            date_filter.append({'main_events.start_date': {
                '$gt': start_date
            }})
        events.find({
            '$or': date_filter
        })


def get_active_event():
    return events.find_one({"main_events.active": True})


print(seats.find_one({'_id': fetch_seat(2019, "Roald Dahl's Matilda the Musical", datetime(2020, 2, 27), 'A', 4)}))
