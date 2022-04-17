from django.urls import path

from . import views

app_name = 'organizer'
urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path("makeParty", views.GetParty, name="form"),
    path("addAvil", views.GetAvil, name="addAvil"),
    path('watchparties', views.WatchParties.as_view(), name='watchparties'),
    path('addMovie', views.addMovie, name='addMovie'),
    path('addUser', views.addUser, name='addUser'),
    path('<int:pk>/', views.DetailView, name='detail'),
]
