from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
# from .views import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import models


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True,
                             help_text='Required. Please use a valid Ridley College Email.')

    class Meta:
        model = models.User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        a = email.endswith("@ridleycollege.com")
        b = User.objects.filter(email__iexact=email)
        if not a or len(b) == 0:
            raise forms.ValidationError("Please use a valid email @ridleycollege.com")
        elif a and len(b) == 0 and len(models.User.objects.filter(email=email)) == 1:
            user = models.User.objects.filter(email=email)[0]
            if user.is_active:
                raise forms.ValidationError("Account with this email already exists.")
            else:
                raise forms.ValidationError(
                    'An email with activation button has been sent to your email, please activate your account!')

        return email


class PurchaseTicket(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ['SessionID']


class EmailForm2(forms.Form):
    Send_all_tickets_in_one_email = forms.BooleanField(required=False)


class EmailForm(forms.Form):
    Email = forms.EmailField()
    Send_all_tickets_in_one_email = forms.BooleanField(required=False)

    def clean_Email(self, *args, **kwargs):
        email = self.cleaned_data['Email'].lower().strip()
        if email not in [i.lower() for i in User.objects.values_list('email', flat=True)]:
            raise forms.ValidationError("Please use a valid email!")
        return email


class EmailForm1(forms.Form):
    Email = forms.EmailField()

    def clean_Email(self, *args, **kwargs):
        email = self.cleaned_data['Email'].lower().strip()
        if email not in [i.lower() for i in User.objects.values_list('email', flat=True)]:
            raise forms.ValidationError("Please use a valid email!")
        return email


class Main_Event_Form(forms.Form):
    Choices = MainEvent.objects.filter(Active=True)


class Each_Event_Form(forms.Form):
    def __init__(self, MainEvent, *args, **kwargs):
        super(Each_Event_Form, self).__init__(*args, **kwargs)
        self.MainEvent = MainEvent.get('Select_an_Event')
        Choices2 = EachEvent.objects.filter(MainEventName=self.MainEvent)

    Select_a_Date_and_Time = forms.ChoiceField()


class seat_list_form(forms.Form):
    def __init__(self, Choices2, *args, **kwargs):
        super(seat_list_form, self).__init__(*args, **kwargs)
        Choice = []
        for i in Choices2:
            Choice.append((str(i), str(i)))
        self.fields['seat'] = forms.MultipleChoiceField(
            required=True,
            widget=forms.CheckboxSelectMultiple(),
            choices=Choice)

    seat = forms.MultipleChoiceField()
