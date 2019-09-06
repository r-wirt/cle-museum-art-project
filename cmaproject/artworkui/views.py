from django.shortcuts import render
from django.http import HttpResponse
import json


def artworkview(request):
    #Import art data
    with open('artworkui/artwork.json') as file:
        data = json.load(file)

    context = {'artwork': data['artworkdata'] }

    return render(request, 'artworkui/main.html', context )
