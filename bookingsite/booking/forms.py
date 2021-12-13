from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from .models import *
import datetime

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class BookingForm (forms.ModelForm):

    def clean_arrival_date(self):
        self.arrival_date = self.cleaned_data['arrival_date']
        if self.arrival_date <= datetime.date.today():
            raise ValidationError('You can`t create booking in past')
        return self.arrival_date

    def clean_departure_date(self):
        departure_date = self.cleaned_data['departure_date']
        if departure_date <= self.arrival_date:
            raise ValidationError('Departure date can`t be less than arrival date')
        return departure_date

    class Meta:
        model = Booking
        fields = '__all__'
