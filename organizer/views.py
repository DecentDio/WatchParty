from django.shortcuts import get_object_or_404, render

def login(request):
    return render(request, 'organizer/login.html', {})