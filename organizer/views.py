from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import WatchParty, AvailabilityRange

def login(request):
    return render(request, 'organizer/login.html', {})

class WatchParties(generic.ListView):
    template_name = 'organizer/watchparties.html'
    context_object_name = 'watchparties_list'
    def get_queryset(self):
        return WatchParty.objects.order_by('title_text')