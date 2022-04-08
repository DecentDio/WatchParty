from django.forms import ModelForm, Textarea, DateInput
from .models import Watchparty, AddedUser, AvailabilityRange, MovieSearcher


class CreateWatchParty(ModelForm):
    class Meta:
        model = Watchparty
        fields = "__all__"
        widgets = {
            'Title': Textarea(),
            'Start Date(YYYY-MM-DD)': Textarea(),
            'End Date (YYYY-MM-DD': Textarea()
        }


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


class CreateMovieSearch(ModelForm):
    class Meta:
        model = MovieSearcher
        fields = "__all__"
        widgets = {
            'Movie Title:': Textarea()
        }
