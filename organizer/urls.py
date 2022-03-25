from django.urls import path

from . import views

app_name = 'organizer'
urlpatterns = [
    path('', views.login, name='login'),
    path('watchparties', views.WatchParties.as_view(), name='watchparties'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]