from django.urls import path
from . import views


urlpatterns = [

    path('', views.artworkview, name="artwork-view")

]
