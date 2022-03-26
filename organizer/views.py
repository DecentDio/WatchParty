from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .forms import CreateWatchParty, CreateAddedUser, CreateAvailabilityRange
from django.http import HttpResponseRedirect
from .models import Watchparty, AvailabilityRange
from django.urls import reverse
from django.utils import timezone


def login(request):
    return render(request, 'organizer/login.html', {})


class WatchParties(generic.ListView):
    template_name = 'organizer/watchparties.html'
    context_object_name = 'watchparties_list'

    def get_queryset(self):
        return Watchparty.objects.order_by('title_text')


class DetailView(generic.DetailView):
    model = Watchparty
    template_name = 'organizer/detail.html'


def GetParty(request):
    if request.method == "POST":
        form = CreateWatchParty(request.POST)
        form.save()
        return redirect("/addUsers")
    else:
        form = CreateWatchParty()
    return render(request, "organizer/check.html", {"form": form})


def GetAdded(request):
    if request.method == "POST":
        form = CreateAddedUser(request.POST)
        form.save()
        return redirect("/addAvil")
    else:
        form = CreateAddedUser()
    return render(request, "organizer/addedUsers.html", {"form": form})


def GetAvil(request):
    if request.method == "POST":
        form = CreateAvailabilityRange(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/watchparties")
    else:
        form = CreateAvailabilityRange()
    return render(request, "organizer/avilPost.html", {"form": form})
