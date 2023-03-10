from django.forms import ModelForm, Textarea, DateInput
from .models import Watchparty, AddedUser, AvailabilityRange, MovieSearcher, Comment
from .widget import DatePickerInput, DateTimePickerInput
from django import forms


class CreateWatchParty(ModelForm):
    class Meta:
        model = Watchparty
        fields = "__all__"
        widgets = {
            'Title': Textarea(),
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'})
        }
        exclude = ['account']


class CreateAddedUser(ModelForm):
    class Meta:
        model = AddedUser
        fields = "__all__"


class CreateAvailabilityRange(ModelForm):
    class Meta:
        model = AvailabilityRange
        fields = "__all__"
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%H:%M')
        }
        exclude = ['account', 'watchparty']


class CreateMovieSearch(ModelForm):
    class Meta:
        model = MovieSearcher
        fields = "__all__"
        widgets = {
            'Movie Title:': Textarea()
        }

class CreateComment(ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        widgets = {
            'text': Textarea()
        }
        exclude = ['account', 'watchparty']

class DateTimeForm(forms.Form):
    date_field = forms.DateField(widget=DatePickerInput, required=False)
    date_time_field = forms.DateTimeField(widget=DateTimePickerInput, required=False)