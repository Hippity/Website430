from django.shortcuts import render , redirect
from django.contrib.auth import login, authenticate, logout
from .forms import NewUserForm
from .models import Book
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
	listBooks = Book.objects.all()
	listBooks = listBooks[0:4]
	if request.user.is_superuser:
		return 	render(request,'super.html')
	return render(request,'index.html',{'listBooks':listBooks})

def logout_request(request):
	listBooks = Book.objects.all()
	listBooks = listBooks[0:4]
	logout(request)
	return render(request,"index.html",{'listBooks':listBooks})


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("index.html")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index.html")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"form":form})