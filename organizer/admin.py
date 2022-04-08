from django.contrib import admin
from .models import Watchparty, AddedUser, AvailabilityRange, MovieSearcher
# Register your models here.

admin.site.register(Watchparty)
admin.site.register(AddedUser)
admin.site.register(AvailabilityRange)
admin.site.register(MovieSearcher)
