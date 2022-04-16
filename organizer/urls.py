from django.urls import path

from . import views

app_name = 'organizer'
urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path("makeParty", views.GetParty, name="form"),
    path("addUsers", views.GetAdded, name="users"),
    path("addAvil", views.GetAvil, name="avil"),
    path('watchparties', views.WatchParties.as_view(), name='watchparties'),
    path('moviesearch', views.MovieSearch, name='movies'),
    path('listOfMovies', views.MovieIMDB.as_view(), name='list'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]
