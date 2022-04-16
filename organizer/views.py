from imdb import Cinemagoer
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .forms import CreateWatchParty, CreateAddedUser, CreateAvailabilityRange, CreateMovieSearch
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from .models import Watchparty, MovieSearcher, ListOfMovies
from django.urls import reverse
from django.utils import timezone
from collections import Counter
from django.contrib.auth import logout


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
    full = {}
    searchResults = []
    if "search_box" in request.GET:
        searchTerm = request.GET['search_box']
        ia = Cinemagoer()
        realList = ia.search_movie(searchTerm)
        for j in range(len(realList)):
            searchResults.append(realList[j]["title"])

    for movieVote in MovieSearcher.objects.all():
        if (movieVote.watchparty, movieVote.search) in full.keys():
            full[(movieVote.watchparty, movieVote.search)] += 1
        else:
            full[(movieVote.watchparty, movieVote.search)] = 1
    return render(request, "organizer/detail.html", {"watchparty": watchparty, "search": full, "searchResults": searchResults})



def MovieIMDB(request):
    searchResults = []
    if request.method == 'GET':
        searchTerm = request.GET['search_box']
    #lastMovieID = int(MovieSearcher.objects.last().id)
    #movie = MovieSearcher.objects.get(pk=lastMovieID).search
    ia = Cinemagoer()
    realList = ia.search_movie(searchTerm)
    for j in range(len(realList)):
        searchResults.append(realList[j]["title"])
    return render(request, "organizer/listOfMovies.html", {"searchResults": searchResults})


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


def MovieSearch(request):
    if request.method == "POST":
        form = CreateMovieSearch(request.POST)
        form.save()
        #something = form.cleaned_data
        #t = MovieSearcher.objects.last()
        #t.x = something['search']
        #t.save()
        return redirect("/listOfMovies")
    else:
        form = CreateMovieSearch()
    return render(request, "organizer/movie.html", {"form": form})
