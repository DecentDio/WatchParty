from django.contrib import admin

from .models import Watchparty, AddedUser, AvailabilityRange, MovieSearcher, ListOfMovies, FavoriteMovie, FinalizedWatchparty, FriendGroup, FriendGroupMember, Images
# Register your models here.

admin.site.register(Watchparty)
admin.site.register(AddedUser)
admin.site.register(AvailabilityRange)
admin.site.register(MovieSearcher)
admin.site.register(ListOfMovies)
admin.site.register(FavoriteMovie)
admin.site.register(FriendGroup)
admin.site.register(FriendGroupMember)
admin.site.register(FinalizedWatchparty)
admin.site.register(Images)
