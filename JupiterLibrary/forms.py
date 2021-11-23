from django.db.models import fields
from django.forms import ModelForm, widgets
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.fields import DateField
from .models import Book, BorrowedBook, UserInfo

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class NewBookForm(ModelForm):
	
	class Meta:
		model = Book
		fields = ['title','authorFirstName','authorLastName','publisher','date']
		widgets = {
			'date': widgets.DateInput(attrs={'type':'date'})
		}
		fields+=['image','genre', 'synopsis','numberAvailable','numberBorrowed']

		
class NewBorrowedBookForm(ModelForm):

	class Meta:
		model = BorrowedBook
		fields = ['username','title','days']


class NewUserInfoForm(ModelForm):
	class Meta:
		model = UserInfo
		fields = ['email','username','bio','fName','lName']