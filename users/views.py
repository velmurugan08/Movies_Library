import json
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from movie_library.utils import hash_pw, check_pw, create_access_token
from .models import Users
from .serializers import LoginSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Get home page
def home(request):
    return render(request, "users/home.html")


@api_view(["POST"])
def login_user(request: HttpRequest):
    serializer = LoginSerializers(data=request.data)
    if serializer.is_valid():
        user = Users.objects.filter(email=serializer.validated_data["email"]).first()
        if user:
            # check password
            if check_pw(serializer.validated_data["password"], user.password):
                # create a jwt token
                token = create_access_token(user)
                # send the token and status
                return Response({"token": token}, 200)
            return Response({"message": "User/Password invalid"}, 401)
        else:
            return Response({"message": "User/Password invalid"}, 401)
    else:
        return Response({"message": serializer.errors}, 400)


def login(request: HttpRequest):
    if request.method == "POST":
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            user = Users.objects.filter(
                email=serializer.validated_data["email"]
            ).first()
            if user:
                # check password
                # create a jwt token
                # send the token and status
                pass
            else:
                return Response({"message": "User/Password invalid"}, 401)
        else:
            return Response({"message": serializer.errors}, 400)
    else:
        # If request method is not POST, render the login form
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})


# To post the register
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = RegisterForm(data)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = hash_pw(form.cleaned_data["password"])
            user.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = RegisterForm()
        return render(request, "users/register.html", {"form": form})
