from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()                 # creates the user
            return redirect("login")    # go to login page
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
