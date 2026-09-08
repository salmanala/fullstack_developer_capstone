# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, post_review, analyze_review_sentiments
from .models import CarMake, CarModel
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
    return JsonResponse(reviews, safe=False)

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
def add_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            result = post_review(data)
            return JsonResponse({"status": 200, "review": result})
        except Exception as e:
            return JsonResponse({"status": 500, "message": str(e)}, status=500)

    return JsonResponse({"status": 405, "message": "POST request required"}, status=405)

def logout_request(request):
    logout(request)
    return JsonResponse({"userName": "", "status": "Logged out"})


def get_dealers(request):
    dealers = get_request("/fetchDealers")
    return JsonResponse(dealers, safe=False)


def get_dealer_by_id(request, dealer_id):
    dealer = get_request(f"/fetchDealer/{dealer_id}")
    return JsonResponse(dealer, safe=False)


def get_dealers_by_state(request, state):
    dealers = get_request(f"/fetchDealers/{state}")
    return JsonResponse(dealers, safe=False)


def get_cars(request):
    car_makes = CarMake.objects.all()
    result = []

    for make in car_makes:
        models = CarModel.objects.filter(car_make=make)

        result.append({
            "make": make.name,
            "description": make.description,
            "CarModels": [
                {
                    "name": model.name,
                    "type": model.type,
                    "year": model.year
                }
                for model in models
            ]
        })

    return JsonResponse(result, safe=False)


def analyze_review(request):
    text = request.GET.get("text", "")
    result = analyze_review_sentiments(text)
    return JsonResponse(result, safe=False)
