from imdb import Cinemagoer
from django.db import models
from django.contrib.auth.models import User


class Watchparty(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    title_text = models.CharField(max_length=200)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)

    def __str__(self):
        return self.title_text

    def valid_date_range(self):
        return self.end_date >= self.start_date


class AddedUser(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    watchparty = models.ForeignKey(Watchparty, on_delete=models.CASCADE)
    def __str__(self):
        return self.account.username + " in " + self.watchparty.title_text


class AvailabilityRange(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    watchparty = models.ForeignKey(Watchparty, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now=False)
    end_time = models.DateTimeField(auto_now=False)

    def valid_time_range(self):
        if self.end_time <= self.start_time:
            return False
        if self.watchparty.start_date.strftime('%Y-%m-%d') > self.start_time.strftime('%Y-%m-%d') or self.watchparty.end_date.strftime('%Y-%m-%d') < self.end_time.strftime('%Y-%m-%d'):
            return False
        return True
    def __str__(self):
        return self.account.username + "'s range for " + self.watchparty.title_text


class MovieSearcher(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    watchparty = models.ForeignKey(Watchparty, on_delete=models.CASCADE)
    search = models.CharField(max_length=100)

    def __str__(self):
        return self.account.username + " votes for " + self.search + " in " + self.watchparty.title_text


class ListOfMovies(models.Model):
    x = models.CharField(max_length=100)


class FavoriteMovie(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.CharField(max_length=200)
    def __str__(self):
        return self.movie

class Comment(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    watchparty = models.ForeignKey(Watchparty, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.account.username + "'s comment in " + self.watchparty.title_text + " on " + self.pub_date
