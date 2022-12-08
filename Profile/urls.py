from django.urls import path
from Profile.views import Login, Registraion

urlpatterns = [
    path('login', Login, name='login'),
    path('registration', Registraion, name='registration')
]