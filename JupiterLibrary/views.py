from django.shortcuts import render , redirect
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.models import User
from .forms import NewBorrowedBookForm, NewUserForm , NewBookForm , NewUserInfoForm
from .models import Book, BorrowedBook, UserInfo 
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

					
			
def makeInfo(request):
	form = NewUserInfoForm()
	userInfos = UserInfo.objects.all()
	users = [info.username for info in userInfos]
	if request.method == 'POST':
		if 'create' in request.POST:
			bio = request.POST['bio']
			fName = request.POST['fName']
			lName = request.POST['lName']
			username = request.user.username
			email = request.user.email
			if username not in users:
				info = NewUserInfoForm({'email':email,'username':username,'bio':bio})
				info.save()
				return index(request)
			else:
				info = UserInfo.objects.get(username=username)
				info.bio = bio
				info.fName= fName
				info.lName=lName
				info.save()
				return index(request)

	return render(request,'makeInfo.html',{'form':form})

@csrf_exempt
def userpage(request):
	msg = 'None'
	userInfos = UserInfo.objects.all()
	users = [info.username for info in userInfos]
	if request.user.username not in users:
		return makeInfo(request)
	instance = UserInfo.objects.get(username=request.user.username)
	if request.method == 'POST':
		if 'del' in request.POST:
			borrowedBooks = BorrowedBook.objects.all()
			msg = 'None'
			myBooks = []
			for book in borrowedBooks:
				if book.username == request.user.username:
					myBooks.append(book)
			if len(myBooks ) == 0:
				instance = UserInfo(username = request.user.username)
				instance.delete()
				user = User.objects.get(username = request.user.username)
				user.delete()
				return index(request)
			else:
				msg = 'Err'
	return render(request, "userpage.html",{'info':instance, 'msg':msg})

@csrf_exempt
def explore(request):
	listBooks = Book.objects.all()
	instance = ''
	exists = ''
	if 'search' in request.POST:
		exists='YES'
		search = True
		bookTitles = [book.title for book in listBooks]
		title = request.POST['searchBook']
		if title in bookTitles:
			instance = Book.objects.get(title=title)
		else:
			exists = 'NO'	
	
	if 'view' in request.POST:
		title = request.POST['whatToView']
		return bookPage(request,title)

	return render(request,"explore.html",{'bookList':listBooks,'result':instance,'exists' : exists})

def bookPage(request,title):
	instance = Book.objects.get(title=title)
	return render(request,'bookPage.html',{'book':instance})
@csrf_exempt
def borrow(request):
	listBooks = Book.objects.all()
	username = request.user.username
	borrowedBooks = BorrowedBook.objects.all()
	msg = 'None'
	myBooks = []
	for book in borrowedBooks:
		if book.username == username:
			myBooks.append(book)

	numBorrowed = len(myBooks)
	myBooksTitles = [book.title for book in myBooks]
	if request.method == 'POST':
		if 'borrow' in request.POST:
			print(request.POST)
			title =  request.POST['searchBook']
			instance = Book.objects.get(title=title)
			if title in myBooksTitles:
				msg = "Err1"
			elif instance.numberBorrowed == instance.numberAvailable:
				msg = 'Err2'
			else:
				borrow = NewBorrowedBookForm(
				{'username' : username,
				'title' :title,
				'days' : 10}
				)
				instance.numberBorrowed += 1
				instance.save()
				borrow.save()
				msg = 'Done1'

		if 'return' in request.POST:
			title =  request.POST['searchBook2']
			instance = BorrowedBook.objects.get(title=title, username=username)
			instance2 = Book.objects.get(title=title)
			instance2.numberBorrowed -= 1
			instance2.save()
			instance.delete()
			msg = 'Done2'

	return render(request,"borrow.html",{'bookList':listBooks , 'borrowedBooks':myBooks , 'numBorrowed': numBorrowed , 'msg':msg})

def statuses(request):
	if request.user.is_superuser:
		borrowedBooks = BorrowedBook.objects.all()
		overdue = []
		notOverdue = []
		for book in borrowedBooks:
			if book.days > 0:
				notOverdue.append(book)
			else:
				overdue.append(book)

		return render(request,"statuses.html", {'overdue':overdue, 'notOverdue':notOverdue})
	else:
		return index(request)