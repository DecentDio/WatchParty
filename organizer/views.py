from imdb import Cinemagoer
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .forms import CreateWatchParty, CreateAddedUser, CreateAvailabilityRange, CreateMovieSearch
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from .models import Watchparty, MovieSearcher, ListOfMovies
from django.urls import reverse
from django.utils import timezone
from collections import Counter


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
    full = {}
    c = Counter(MovieSearcher.objects.values_list('search'))
    for i in MovieSearcher.objects.values_list('search'):
        full[i] = c[i]
    extra_context = {'search': full}


class MovieIMDB(generic.ListView):
    model = ListOfMovies
    template_name = 'organizer/listOfMovies.html'
    movie = ""
    whatever = []
    for i in ListOfMovies.objects.values_list('x'):
        movie = i[0]
    ia = Cinemagoer()
    realList = ia.search_movie(movie)
    for j in range(len(realList)):
        whatever.append(realList[j]["title"])
    extra_context = {'xy': whatever}

    def post(self, request):
        myVar = request.POST.get("movies")
        s = MovieSearcher.objects.latest('search')
        s.search = myVar
        s.save()
        return redirect("/watchparties")


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
        something = form.cleaned_data
        t = ListOfMovies.objects.get()
        t.x = something['search']
        t.save()
        return redirect("/listOfMovies")
    else:
        form = CreateMovieSearch()
    return render(request, "organizer/movie.html", {"form": form})
