import os

from django.shortcuts import get_object_or_404, render
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view

from .forms import *
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import models
from .serializers import SeatSerializer
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import *
from scripts.qr_code.generate_qr_code import *
import json
import uuid
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import *
from .models import User
from .serializers import SeatSerializer
from scripts.qr_code.generate_qr_code import GenerateQR
from django.contrib import auth
from rest_framework import viewsets
from rest_framework import status
from django.http import Http404


def purchase(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            SessionID = 0
            post_request = PurchaseTicket(request.POST or None)
            if post_request.is_valid():
                Session = post_request.cleaned_data['SessionID']
                arr = EachEvent.objects.all()
                for i in arr:
                    if str(i) == str(Session):
                        SessionID = i.id
                url = '/tickets/seat_selection/' + str(SessionID)
                return HttpResponseRedirect(url)
        else:
            form = PurchaseTicket()
        event_id = max(MainEvent.objects.values_list('pk', flat=True))
        event = MainEvent.objects.get(id=event_id)
        event_start_date = event.StartDate
        event_end_date = event.EndDate

        context = {'form': form, 'event_name': event, 'event_start_date': event_start_date,
                   'event_end_date': event_end_date}
        return render(request, 'tickets/purchase.html', context)
    else:
        return HttpResponseRedirect(reverse('tickets:home'))


def user_signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            email_subject = 'Activate Your Account'
            message = render_to_string('tickets/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': str(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

            return render(request, 'tickets/sent_email_confirmation.html')
    else:
        form = UserSignUpForm()
    return render(request, 'tickets/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = auth.models.User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, auth.models.User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        url = reverse('tickets:home')
        return HttpResponseRedirect(url)
    else:
        return render(request, 'tickets/invalid_link.html')


def seat_selection(request, session):
    if request.user.is_authenticated:
        occupied = list()
        if request.method == 'POST':
            form = request.POST
            seats = form.getlist('seat')
            seats = ' '.join(str(e) for e in seats)
            for r, c in parser(seats):
                obj = Seat.objects.get(SessionID=session, Row=r, Column=c)
                if obj.Occupied:
                    messages.info(request,
                                  'Some of the seats that you previously selected have been occupied! Please select again!')
                    return HttpResponseRedirect('/tickets/seat_selection/' + session)
            url = '/tickets/email/' + session + '/' + seats
            return HttpResponseRedirect(url)
        else:
            occupied0 = Seat.objects.filter(SessionID=session, Occupied=True).values('Row', 'Column')
            for i in occupied0:
                row = i.get('Row')
                col = str(i.get('Column'))
                occupied.append(row + col)
            SessionID = str(EachEvent.objects.get(id=session))
            week = EachEvent.objects.get(id=session).Week
            array = []  # some seats
            for row, column in array:
                for index, i in enumerate(column):
                    column[index] = str(i)
            array = array[::-1]
            array1 = list()
            for row, column in array:
                column = column[::-1]
                array1.append((row, column))
            context = {'title': 'Event', 'heading': 'Ticket Selling System', 'num': '-1', 'num2': '-2',
                       'array': array1, 'Occupied': occupied, 'SessionID': SessionID,
                       'session': session, 'week': week
                       }
            return render(request, 'tickets/seat_selection.html', context)
    else:
        return HttpResponseRedirect(reverse('tickets:home'))


def email(request, session, seats):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            form = EmailForm(request.POST or None)
            if form.is_valid():
                email = form.cleaned_data['Email']
                seats = parser(seats)
                a = GenerateQR()
                user = User.objects.filter(email__iexact=email).first()
                if not form.cleaned_data['Send_all_tickets_in_one_email']:
                    for r, c in seats:
                        obj = Seat.objects.get(SessionID=session, Row=r, Column=c)
                        if obj.Occupied:
                            messages.info(request,
                                          'Some of the seats that you previously selected have been occupied! Please select again!')
                            return HttpResponseRedirect('/tickets/seat_selection/' + session)
                    for row, col in seats:
                        obj = Seat.objects.get(SessionID=session, Row=row, Column=col)
                        obj.CustomerID = user
                        obj.Occupied = True
                        string = email + str(obj)
                        qr = str(uuid.uuid5(uuid.NAMESPACE_DNS, string))
                        obj.Qr_String = qr
                        obj.save(update_fields=['CustomerID', 'Occupied', 'Qr_String'])
                        email_subject = 'Ticket'
                        message = render_to_string('tickets/qrcode.html', {
                            'user': user,
                            'SessionID': obj.SessionID,
                            'Row': obj.Row,
                            'Column': obj.Column,
                        })
                        msg = EmailMessage(email_subject, message, to=[email])
                        msg.attach_file(a.generate(obj.Qr_String))
                        msg.content_subtype = "html"
                        msg.send()
                        try:
                            os.remove('qrcode/' + obj.Qr_String + '.png')
                        except:
                            print("Error: " + obj.Qr_String)
                else:
                    for r, c in seats:
                        obj = Seat.objects.get(SessionID=session, Row=r, Column=c)
                        if obj.Occupied:
                            messages.info(request,
                                          'Some of the seats that you previously selected have been occupied! Please select again!')
                            return HttpResponseRedirect('/tickets/seat_selection/' + session)

                    email_subject = 'Ticket'
                    seat = []
                    objects = []
                    for row, col in seats:
                        obj = Seat.objects.get(SessionID=session, Row=row, Column=col)
                        obj.CustomerID = user
                        obj.Occupied = True
                        string = email + str(obj)
                        qr = str(uuid.uuid5(uuid.NAMESPACE_DNS, string))
                        obj.Qr_String = qr
                        obj.save(update_fields=['CustomerID', 'Occupied', 'Qr_String'])
                        objects.append(obj)
                        seat.append(obj.Row + str(obj.Column))
                    message = render_to_string('tickets/qrcode.html', {
                        'user': user,
                        'SessionID': objects[0].SessionID,
                        'Row': ', '.join(sorted(seat))
                    })
                    msg = EmailMessage(email_subject, message, to=[email])
                    for obj in objects:
                        msg.attach_file(a.generate(obj.Qr_String))
                    msg.content_subtype = "html"
                    msg.send()
                    for obj in objects:
                        try:
                            os.remove('qrcode/' + obj.Qr_String + '.png')
                        except:
                            print("Error: " + obj.Qr_String)
                url = '/tickets/success'
                return HttpResponseRedirect(url)
        else:
            form = EmailForm()
        context = {
            'form': form,
            'session': session,
            'seats': seats,
            'site': 'email/' + session + '/' + seats,

        }
        return render(request, "tickets/seat_email.html", context)
    elif request.user.is_authenticated and not request.user.is_staff:
        if request.method == "POST":
            form = EmailForm2(request.POST or None)
            if form.is_valid():
                email = request.user.email
                seats = parser(seats)
                a = GenerateQR()
                user = User.objects.filter(email__iexact=email).first()
                if not form.cleaned_data['Send_all_tickets_in_one_email']:
                    for r, c in seats:
                        obj = Seat.objects.get(SessionID=session, Row=r, Column=c)
                        if obj.Occupied:
                            messages.info(request,
                                          'Some of the seats that you previously selected have been occupied! Please select again!')
                            return HttpResponseRedirect('/tickets/seat_selection/' + session)
                    for row, col in seats:
                        obj = Seat.objects.get(SessionID=session, Row=row, Column=col)
                        obj.CustomerID = user
                        obj.Occupied = True
                        string = email + str(obj)
                        qr = str(uuid.uuid5(uuid.NAMESPACE_DNS, string))
                        obj.Qr_String = qr
                        obj.save(update_fields=['CustomerID', 'Occupied', 'Qr_String'])
                        email_subject = 'Ticket'
                        message = render_to_string('tickets/qrcode.html', {
                            'user': user,
                            'SessionID': obj.SessionID,
                            'Row': obj.Row,
                            'Column': obj.Column,
                        })
                        msg = EmailMessage(email_subject, message, to=[email])
                        msg.attach_file(a.generate(obj.Qr_String))
                        msg.content_subtype = "html"
                        msg.send()
                        try:
                            os.remove('qrcode/' + obj.Qr_String + '.png')
                        except:
                            print("Error: " + obj.Qr_String)
                else:
                    for r, c in seats:
                        obj = Seat.objects.get(SessionID=session, Row=r, Column=c)
                        if obj.Occupied:
                            messages.info(request,
                                          'Some of the seats that you previously selected have been occupied! Please select again!')
                            return HttpResponseRedirect('/tickets/seat_selection/' + session)

                    email_subject = 'Ticket'
                    seat = []
                    objects = []
                    for row, col in seats:
                        obj = Seat.objects.get(SessionID=session, Row=row, Column=col)
                        obj.CustomerID = user
                        obj.Occupied = True
                        string = email + str(obj)
                        qr = str(uuid.uuid5(uuid.NAMESPACE_DNS, string))
                        obj.Qr_String = qr
                        obj.save(update_fields=['CustomerID', 'Occupied', 'Qr_String'])
                        objects.append(obj)
                        seat.append(obj.Row + str(obj.Column))
                    message = render_to_string('tickets/qrcode.html', {
                        'user': user,
                        'SessionID': objects[0].SessionID,
                        'Row': ', '.join(sorted(seat))
                    })
                    msg = EmailMessage(email_subject, message, to=[email])
                    for obj in objects:
                        msg.attach_file(a.generate(obj.Qr_String))
                    msg.content_subtype = "html"
                    msg.send()
                    for obj in objects:
                        try:
                            os.remove('qrcode/' + obj.Qr_String + '.png')
                        except:
                            print("Error: " + obj.Qr_String)
                url = '/tickets/success'
                return HttpResponseRedirect(url)
        else:
            form = EmailForm()
        context = {
            'form': form,
            'session': session,
            'seats': seats,
            'site': 'email/' + session + '/' + seats,

        }
        return render(request, "tickets/seat_email.html", context)
    else:
        return HttpResponseRedirect(reverse('tickets:home'))


def success(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, "tickets/success.html", context)
    else:
        return HttpResponseRedirect(reverse('tickets:home'))


def modify(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            form = EmailForm1(request.POST or None)
            if form.is_valid():
                email = form.cleaned_data['Email']
                return HttpResponseRedirect('seat_list/' + email)
        else:
            form = EmailForm1()
        context = {
            'form': form,
            'site': 'modify',
        }
        return render(request, "tickets/seat_email.html", context)
    elif request.user.is_authenticated and not request.user.is_staff:
        return HttpResponseRedirect('seat_list/' + request.user.email)
    else:
        return HttpResponseRedirect(reverse('tickets:home'))


def seat_list(request, email):
    if request.user.is_authenticated and request.user.is_staff:
        seats = list()
        if request.method == "POST":
            form = request.POST
            seats = form.getlist('seats')
            for j in range(len(seats)):
                temp = parse(seats[j])
                seat = Seat.objects.filter(SessionID=temp[0]).filter(Column__icontains=temp[2]).filter(Row=temp[1])
                for i in seat:
                    i.CustomerID = None
                    i.Occupied = False
                    i.Qr_String = None
                    i.Scanned = False
                    i.save()
                # seat.update(CustomerID = None,Occupied = False,Qr_String = None,Scanned = False)
            return HttpResponseRedirect('/tickets/success')
        user = User.objects.filter(email__iexact=email).first()
        seats0 = Seat.objects.filter(CustomerID=user)
        for i in seats0:
            seats.append(str(i))
        context = {
            'email': email,
            'list': seats,
        }
        return render(request, "tickets/seat_list.html", context)
    elif request.user.is_authenticated and not request.user.is_staff:
        if email == request.user.email:
            seats = list()
            user = User.objects.filter(email__iexact=email).first()
            seats0 = Seat.objects.filter(CustomerID=user)
            for i in seats0:
                seats.append(str(i))
            context = {
                'email': email,
                'list': seats,
            }
            return render(request, "tickets/seat_list.html", context)
        else:
            return HttpResponseRedirect(reverse('tickets:home'))
    else:
        return HttpResponseRedirect(reverse('tickets:home'))


def parser(string):
    b = []
    for i in string.split(" "):
        row = i[:1]
        col = i[1:len(i)]
        col = int(col)
        b.append((row, col))
    return b
