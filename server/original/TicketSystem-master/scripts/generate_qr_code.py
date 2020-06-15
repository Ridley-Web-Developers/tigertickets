import uuid
from MyQR import myqr
from tickets.models import *


class GenerateQR:
    def __init__(self):
        self.main_event = MainEvent
        self.each_event = EachEvent
        self.seat = Seat
        self.user = User

    def generate(self, string):
        version, level, qr_name = myqr.run(
            words=string,
            version=3,
            level='H',
            picture=None,
            colorized=False,
            contrast=1.0,
            brightness=1.0,
            save_name=string+'.png',
            save_dir='qrcode'
        )
        return qr_name


def convert(event_id, session_id, date, customer_id, last_name, first_name, email_address, row, column):
    return '-'.join([event_id, session_id, date, customer_id, last_name, first_name, email_address, row, column])
