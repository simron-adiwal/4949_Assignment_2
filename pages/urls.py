# pages/urls.py
from django.urls import path, include
from .views import homePageView, aboutPageView, simronPageView, results, homePost, todos, register, message, secretArea

urlpatterns = [
    path('', homePageView, name='home'),
    path('about/', aboutPageView, name='about'),
    path('simron/', simronPageView, name='simron'),
    path('homePost/', homePost, name='homePost'),
    path('<int:choice>/results/', results, name='results'),
    path('results/<int:choice>/<str:gmat>/', results, name='results'),
    path('results/<str:educ>/<str:unemployment>/<str:dist>/<str:tuition>', results,
         name='results'),
    path('todos', todos, name='todos'),
    path("register/", register, name="register"),  # <-- added
    path('message/<str:msg>/<str:title>/', message, name="message"),  # <-- added
    path('', include("django.contrib.auth.urls")), # <-- added
    path("secret/", secretArea, name="secret"),
]
