from django.shortcuts import render , redirect
from django.contrib.auth import login, authenticate, logout
from .forms import NewUserForm , NewBookForm
from .models import Book
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from json import dump, dumps
from datetime import datetime


# Create your views here.
def index(request):
	listBooks = Book.objects.all()
	total = len(listBooks)
	listBooks = listBooks[total-4:total]
	if request.user.is_superuser:
		return 	render(request,'super.html')
	return render(request,'index.html',{'listBooks':listBooks})

def logout_request(request):
	listBooks = Book.objects.all()
	total = len(listBooks)
	listBooks = listBooks[total-4:total]
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

def addEdit(request):
	if request.user.is_superuser:
		listBooks = Book.objects.all()
		exists = 'Nothing'
		if request.method == 'POST':
				form = NewBookForm(request.POST,request.FILES)
				bookTitles = [book.title for book in listBooks]
				print(request.FILES)
				if request.POST['title'] in bookTitles:
					exists = 'Yes'
				if exists == 'Nothing':
					if form.is_valid():
						exists = 'No'
						form.save()
		form = NewBookForm() 
		return render(request,'addEdit.html', {'bookList': listBooks , 'exists' : exists,'form' : form})
	else:
		return index(request)

def userpage(request):
	return render(request, "userpage.html")

def explore(request):
	return render(request,"explore.html")