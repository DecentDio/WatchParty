from django.urls import path

from . import views

app_name = 'organizer'
urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path("makeParty", views.GetParty, name="form"),
    path("addAvil", views.GetAvil, name="addAvil"),
    path('watchparties', views.WatchParties, name='watchparties'),
    path('addMovie', views.addMovie, name='addMovie'),
    path('addUser', views.addUser, name='addUser'),
    path('createFriendGroup', views.createFriendGroup, name = 'createFriendGroup'),
    path('<int:pk>/', views.DetailView, name='detail'),
    path('kickUser', views.kickUser, name='kickUser'),
    path('getComment', views.GetComment, name='getComment'),
    path('deleteComment', views.deleteComment, name='deleteComment'),
    path('deleteWatchParties', views.deleteWatchParty, name='deleteWatchParty'),
    path('favorites', views.favoritesView, name='favorites'),
    path('addFav', views.addFavorite, name='addFav'),
    path('rmFav', views.rmFavorite, name='rmFav'),
    path('rmAvilRange', views.rmAvilRange, name='rmAvilRange'),
    path('addFriendGroup', views.addFriendGroup, name='addFriendGroup'),
    path('finalWP', views.finalWP, name='finalWP')
]
