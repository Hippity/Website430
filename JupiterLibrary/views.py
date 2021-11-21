from django.shortcuts import render , redirect
from django.contrib.auth import login, authenticate, logout
from .forms import NewUserForm , NewBookForm
from .models import Book
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from json import dump, dumps
from datetime import datetime
from django.views.generic import (
    CreateView, 
    ListView, 
    UpdateView, 
    DetailView, 
    DeleteView
)
from django.views.decorators.csrf import csrf_exempt,csrf_protect


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

@csrf_exempt
def addEdit(request):
	if request.user.is_superuser:
		listBooks = Book.objects.all()
		exists = 'Nothing'
		formSearch = NewBookForm()
		search=False
		if request.method == 'POST':
				if 'add' in request.POST:
					form = NewBookForm(request.POST,request.FILES)
					bookTitles = [book.title for book in listBooks]
					if request.POST['title'] in bookTitles:
						exists = 'Yes'
					if exists == 'Nothing':
						if form.is_valid():
							exists = 'No'
							form.save()
				if 'search' in request.POST:
					search = True
					bookTitles = [book.title for book in listBooks]
					title = request.POST['searchBook']
					if title in bookTitles:
						instance = Book.objects.get(title=title)
						formSearch = NewBookForm(instance = instance)
					else:
						exists = 'NO'
				if 'Delete' in request.POST:
					title = request.POST['title']
					instance = Book.objects.get(title=title)
					instance.delete()

				if 'Update' in request.POST:
					bookTitles = [book.title for book in listBooks]
					title = request.POST['title']
					if title not in bookTitles:
						exists = 'NO3'
					else:
						instance = Book.objects.get(title=title)
						formSearch = NewBookForm(request.POST, instance = instance)
						if formSearch.is_valid():
							formSearch.save()

		form = NewBookForm() 
		return render(request,'addEdit.html', {'bookList': listBooks , 
		'exists' : exists,'form' : form, "iAmSearching":search, 'searchForm':formSearch})
	else:
		return index(request)

					
			



def userpage(request):
	return render(request, "userpage.html")

def explore(request):
	return render(request,"explore.html")

def bookPage(request):
	listBooks = Book.objects.all()
	return render(request,'bookPage.html',{'book':listBooks[0]})