from imdb import Cinemagoer
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .forms import CreateWatchParty, CreateAddedUser, CreateAvailabilityRange, CreateMovieSearch
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from .models import Watchparty, MovieSearcher, ListOfMovies, AddedUser
from django.urls import reverse
from django.utils import timezone
from collections import Counter
from django.contrib.auth import logout
from django.contrib.auth.models import User


def login(request):
    return render(request, 'organizer/login.html', {})


def logout_view(request):
    logout(request)
    return render(request, 'organizer/login.html', {})


class WatchParties(generic.ListView):
    template_name = 'organizer/watchparties.html'
    context_object_name = 'watchparties_list'

    def get_queryset(self):
        return Watchparty.objects.order_by('title_text')


def DetailView(request, pk):
    watchparty = Watchparty.objects.get(pk=pk)
    searchResults = []
    if "search_box" in request.GET:
        searchTerm = request.GET['search_box']
        ia = Cinemagoer()
        realList = ia.search_movie(searchTerm)
        for j in range(len(realList)):
            searchResults.append(realList[j]["title"])
    return render(request, "organizer/detail.html",
                  {"watchparty": watchparty, "users": User.objects.all(), "search": getMovieVotes(),
                   "searchResults": searchResults, "allowedUsers": getAllowedUsers(watchparty)})


def getAllowedUsers(watchparty):
    allowedUsers = []
    allowedUsers.append(watchparty.account)
    for user in watchparty.addeduser_set.all():
        allowedUsers.append(user.account)
    return allowedUsers


def getMovieVotes():
    full = {}
    for movieVote in MovieSearcher.objects.all():
        if (movieVote.watchparty, movieVote.search) in full.keys():
            full[(movieVote.watchparty, movieVote.search)] += 1
        else:
            full[(movieVote.watchparty, movieVote.search)] = 1
    return full


def GetParty(request):
    if request.method == "POST":
        form = CreateWatchParty(request.POST)
        form.instance.account = request.user
        form.save()
        return redirect("/watchparties")
    else:
        form = CreateWatchParty()
    return render(request, "organizer/check.html", {"form": form})


def GetAvil(request):
    if request.method == "POST":
        form = CreateAvailabilityRange(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/watchparties")
    else:
        form = CreateAvailabilityRange()
    return render(request, "organizer/avilPost.html", {"form": form})


def addUser(request):
    watchpartyID = request.POST['watchpartyID']
    userID = request.POST['userID']
    user = User.objects.get(pk=userID)
    watchparty = Watchparty.objects.get(pk=watchpartyID)
    if AddedUser.objects.filter(account=user, watchparty=watchparty).exists():
        return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))
    au = AddedUser(account=user, watchparty=watchparty)
    au.save()
    return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))


def addMovie(request):
    watchpartyID = request.POST['watchpartyID']
    userID = request.POST['userID']
    user = User.objects.get(pk=userID)
    watchparty = Watchparty.objects.get(pk=watchpartyID)
    if 'movies' not in request.POST:
        return render(request, "organizer/detail.html", {"watchparty": watchparty, "users": User.objects.all(),
                                                         "allowedUsers": getAllowedUsers(watchparty),
                                                         "search": getMovieVotes(),
                                                         "error_message": "Error: No movie selected!"})

    movie = request.POST['movies']

    if MovieSearcher.objects.filter(account=user, watchparty=watchparty, search=movie).exists():
        return render(request, "organizer/detail.html", {"watchparty": watchparty, "users": User.objects.all(),
                                                         "allowedUsers": getAllowedUsers(watchparty),
                                                         "search": getMovieVotes(),
                                                         "error_message": "Error: You already voted for this!"})
    m = MovieSearcher(account=user, watchparty=watchparty, search=movie)
    m.save()
    return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))
