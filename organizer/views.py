from imdb import Cinemagoer
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .forms import CreateWatchParty, CreateAddedUser, CreateAvailabilityRange, CreateMovieSearch, CreateComment
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from .models import Watchparty, MovieSearcher, ListOfMovies, AddedUser, Comment, AvailabilityRange, FavoriteMovie
from django.urls import reverse
from django.utils import timezone
from collections import Counter
from django.contrib.auth import logout
from django.contrib.auth.models import User
import datetime


def login(request):
    return render(request, 'organizer/login.html', {})


def logout_view(request):
    logout(request)
    return render(request, 'organizer/login.html', {})


def WatchParties(request):
    invitedWatchParties = []
    for party in AddedUser.objects.filter(account=request.user):
        invitedWatchParties.append(party.watchparty)
    return render(request,'organizer/watchparties.html',{"watchparties_list":Watchparty.objects.order_by('title_text'), "invitedWatchParties":invitedWatchParties})

def favoritesView(request):
    favorites = dict.fromkeys(FavoriteMovie.objects.filter(account=request.user))
    for movie in favorites.keys():
        sameTaste = FavoriteMovie.objects.filter(movie=movie).exclude(account=request.user)
        favorites[movie] = sameTaste
    searchResults = []
    if "search_box" in request.GET:
        searchResults = searchMovie(request.GET['search_box'])
    return render(request, 'organizer/favorites.html', {"favorites": favorites, "searchResults": searchResults})

def DetailView(request, pk):
    watchparty = Watchparty.objects.get(pk=pk)
    optimalRangesTime = []
    for range in AvailabilityRange.objects.filter(watchparty = watchparty, account = request.user):
        optimalRangesTime.append((range.start_time,range.end_time))

    startAndEndRange = []

    if len(optimalRangesTime) > 0:
        defaultStartTime = optimalRangesTime[0][0]
        defaultEndTime = optimalRangesTime[0][1]
        for i in optimalRangesTime:
            if i[0] > defaultStartTime:
                defaultStartTime = i[0]
            if i[1] > defaultEndTime:
                defaultEndTime = i[1]
        startAndEndRange.append(defaultStartTime)
        startAndEndRange.append(defaultEndTime)
        
    

    searchResults = []
    if "search_box" in request.GET:
        searchResults = searchMovie(request.GET['search_box'])
    return render(request, "organizer/detail.html",
                  {"watchparty": watchparty, "comments": Comment.objects.filter(watchparty=watchparty).order_by("-pub_date"), "users": User.objects.all(), "userVotes": getUsersVotes(request.user),
                   "search": getMovieVotes(), "searchResults": searchResults, "allowedUsers": getAllowedUsers(watchparty), "optimalRange":startAndEndRange})

def searchMovie(searchTerm):
    ia = Cinemagoer()
    searchResultsObjects = ia.search_movie(searchTerm)
    searchResults = []
    for i in range(len(searchResultsObjects)):
        searchResults.append(searchResultsObjects[i]["title"])
    return searchResults

def getAllowedUsers(watchparty):
    allowedUsers = []
    allowedUsers.append(watchparty.account)
    for user in watchparty.addeduser_set.all():
        allowedUsers.append(user.account)
    return allowedUsers

def getUsersVotes(user):
    usersVotes = []
    for movieVote in MovieSearcher.objects.filter(account=user):
        usersVotes.append(movieVote.search)
    return usersVotes

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
        form.instance.account = User.objects.get(pk=request.POST['userID'])
        form.instance.watchparty = Watchparty.objects.get(pk=request.POST['watchpartyID'])
        obj = form.save(commit=False)
        if obj.valid_time_range():
            obj.save()
        return HttpResponseRedirect(reverse('organizer:detail', args=(request.POST['watchpartyID'],)))
    else:
        form = CreateAvailabilityRange()
    return render(request, "organizer/avilPost.html",
                  {"form": form, "watchpartyID": request.GET['watchpartyID'], "userID": request.GET['userID']})


def addUser(request):
    watchpartyID = request.POST['watchpartyID']
    userID = request.POST['userID']
    user = User.objects.get(pk=userID)
    watchparty = Watchparty.objects.get(pk=watchpartyID)
    if watchparty.account.username == user.username:
        return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))
    if AddedUser.objects.filter(account=user, watchparty=watchparty).exists():
        return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))
    au = AddedUser(account=user, watchparty=watchparty)
    au.save()
    return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))


def kickUser(request):
    watchpartyID = request.POST['watchpartyID']
    userID = request.POST['kickedUserID']
    user = User.objects.get(pk=userID)
    watchparty = Watchparty.objects.get(pk=watchpartyID)
    if watchparty.account.username == user.username:
        return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))
    # MODELS TO SEARCH FOR OBJECTS TO DELETE:
    # AddedUser, AvailabilityRange, MovieSearcher, Comment,
    AddedUser.objects.filter(account=user, watchparty=watchparty).delete()
    AvailabilityRange.objects.filter(account=user, watchparty=watchparty).delete()
    MovieSearcher.objects.filter(account=user, watchparty=watchparty).delete()
    Comment.objects.filter(account=user, watchparty=watchparty).delete()
    return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))

def deleteWatchParty(request):
    watchpartyID = request.POST['deletedID']
    Watchparty.objects.get(pk=watchpartyID).delete()
    return HttpResponseRedirect(reverse('organizer:watchparties'))

def addMovie(request):
    watchpartyID = request.POST['watchpartyID']
    userID = request.POST['userID']
    user = User.objects.get(pk=userID)
    watchparty = Watchparty.objects.get(pk=watchpartyID)
    if 'movies' not in request.POST:
        return render(request, "organizer/detail.html", {"watchparty": watchparty, "users": User.objects.all(),
                                                         "userVotes": getUsersVotes(request.user), "allowedUsers": getAllowedUsers(watchparty),
                                                         "search": getMovieVotes(),
                                                         "error_message": "Error: No movie selected!"})

    movie = request.POST['movies']
    if 'rmVote' in request.POST:
        if not MovieSearcher.objects.filter(account=user, watchparty=watchparty, search=movie).exists():
            return render(request, "organizer/detail.html", {"watchparty": watchparty, "users": User.objects.all(),
                                                             "userVotes": getUsersVotes(request.user),
                                                             "allowedUsers": getAllowedUsers(watchparty),
                                                             "search": getMovieVotes(),
                                                             "error_message": "Error: You didn't vote for this!"})
        MovieSearcher.objects.filter(account=user, watchparty=watchparty, search=movie).delete()
        return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))
    if MovieSearcher.objects.filter(account=user, watchparty=watchparty, search=movie).exists():
        return render(request, "organizer/detail.html", {"watchparty": watchparty, "users": User.objects.all(),
                                                         "userVotes": getUsersVotes(request.user), "allowedUsers": getAllowedUsers(watchparty),
                                                         "search": getMovieVotes(),
                                                         "error_message": "Error: You already voted for this!"})
    m = MovieSearcher(account=user, watchparty=watchparty, search=movie)
    m.save()
    return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))

def addFavorite(request):
    movie = request.POST['movie']
    user = User.objects.get(pk=request.POST['userID'])
    if FavoriteMovie.objects.filter(account=user, movie=movie).exists():
        return HttpResponseRedirect(reverse('organizer:favorites'))
    fm = FavoriteMovie(account=user, movie=movie)
    fm.save()
    return HttpResponseRedirect(reverse('organizer:favorites'))

def rmFavorite(request):
    movie = request.POST['movie']
    user = User.objects.get(pk=request.POST['userID'])
    if FavoriteMovie.objects.filter(account=user, movie=movie).exists():
        FavoriteMovie.objects.filter(account=user, movie=movie).delete()
    return HttpResponseRedirect(reverse('organizer:favorites'))

def GetComment(request):
    watchpartyID = request.POST['watchpartyID']
    userID = request.POST['userID']
    user = User.objects.get(pk=userID)
    watchparty = Watchparty.objects.get(pk=watchpartyID)
    comment = request.POST['comment']
    if comment == '':
        return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))
    time = datetime.datetime.now()
    c = Comment(account=user, watchparty=watchparty, text=comment, pub_date=time)
    c.save()
    return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))

def deleteComment(request):
    comment = Comment.objects.get(pk = request.POST['commentID'])
    watchpartyID = comment.watchparty.id
    comment.delete()
    return HttpResponseRedirect(reverse('organizer:detail', args=(watchpartyID,)))
