from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    school_id = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=140)

    def __str__(self):
        return '%s, %s' % (self.first_name, self.last_name)


class Event(models.Model):
    title = models.CharField(max_length=140)
    subtitle = models.CharField(max_length=140)
    image = models.ImageField(upload_to='images/event_images/')
    preview_image = models.ImageField(upload_to='images/event_preview/', blank=True)
    body = models.TextField()
    date = models.DateField()
    additional = models.TextField(blank=True, default='')
    photo_link = models.CharField(max_length=300, blank=True, default='')
    video_link = models.CharField(max_length=300, blank=True, default='')
    related_links = models.TextField(blank=True, default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Event Information'
        verbose_name_plural = 'Event Information'


class MainEvent(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.TextField(unique=True)
    StartDate = models.DateField()
    EndDate = models.DateField()
    Active = models.BooleanField(default=False)

    def __str__(self):
        return self.Name


class EachEvent(models.Model):
    id = models.AutoField(primary_key=True)
    MainEventName = models.ForeignKey(MainEvent, on_delete=models.CASCADE)
    SessionDate = models.DateField(unique=True)
    Week = models.CharField(max_length=10, null=True)

    def __str__(self):
        return '{name}, {date} - {week}'.format(name=self.MainEventName, date=self.SessionDate, week=self.Week)


class Seat(models.Model):
    SessionID = models.ForeignKey(EachEvent, on_delete=models.CASCADE)
    CustomerID = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    Row = models.CharField(max_length=1)
    Column = models.IntegerField()
    Occupied = models.BooleanField(default=False)  # if the seat is selected(occupied)
    Scanned = models.BooleanField(default=False)  # if the ticket of this seat is scanned
    Qr_String = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{SessionID}, {Row},{Column}'.format(SessionID=self.SessionID, Row=self.Row, Column=self.Column)
